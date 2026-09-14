#!/usr/bin/env python3
"""Bangkok Site Engineer job pipeline.

Collects, deduplicates, scores and reports Site Engineer openings in the Bangkok
metropolitan area posted within the last N days.  Re-runnable: results are
upserted into output/jobs.sqlite keyed by a stable id, so daily runs append
without creating duplicates.

    python run.py --days 5
"""
from __future__ import annotations

import argparse, csv, hashlib, json, logging, re, sqlite3, sys, time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urljoin, quote_plus, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup
from rapidfuzz import fuzz

import sources as S
from parsing import (canonical_role, company_type, detect_lang, find_district,
                     norm_company, parse_date, parse_experience, parse_salary, score)
from reporting import ASSUMPTIONS, report

LOG = logging.getLogger("jobs")
ROOT = Path(__file__).resolve().parent
FIELDS = ["id", "title", "title_norm", "company", "company_type", "district",
          "posted_date", "date_unknown", "salary_min", "salary_max", "salary_text",
          "experience_years", "language_of_post", "requirements_summary", "url",
          "alt_urls", "source", "relevance_score", "scraped_at"]
MIN_SCORE = 30
THAI = re.compile(r"[฀-๿]")


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #
class Http:
    """Polite fetcher: >=2s between hits on one host, robots.txt honoured."""

    def __init__(self, delay=2.0, timeout=25):
        self.delay, self.timeout = delay, timeout
        self.session = requests.Session()
        self.session.headers.update(S.HEADERS)
        self._last: dict[str, float] = {}
        self._robots: dict[str, RobotFileParser | None] = {}

    def _wait(self, host):
        gap = time.time() - self._last.get(host, 0.0)
        if gap < self.delay:
            time.sleep(self.delay - gap)
        self._last[host] = time.time()

    def allowed(self, url):
        host = urlparse(url).netloc
        if host not in self._robots:
            rp = RobotFileParser()
            robots_url = f"{urlparse(url).scheme}://{host}/robots.txt"
            try:
                self._wait(host)
                r = self.session.get(robots_url, timeout=self.timeout)
                if r.status_code >= 500:           # server error -> treat as disallow
                    self._robots[host] = "deny"
                elif r.status_code >= 400:         # absent -> everything allowed
                    self._robots[host] = None
                else:
                    rp.parse(r.text.splitlines())
                    self._robots[host] = rp
            except requests.RequestException:
                self._robots[host] = None          # unreachable -> unknown, attempt once
        rp = self._robots[host]
        if rp == "deny":
            return False
        if rp is None:
            return True
        return rp.can_fetch(S.HEADERS["User-Agent"], url)

    def get(self, url):
        """Return (status_code, text, error_string)."""
        host = urlparse(url).netloc
        if not self.allowed(url):
            return None, None, "disallowed by robots.txt"
        try:
            self._wait(host)
            r = self.session.get(url, timeout=self.timeout)
            return r.status_code, r.text, None
        except requests.RequestException as exc:
            return None, None, f"{type(exc).__name__}: {str(exc)[:160]}"

    def verify(self, url):
        host = urlparse(url).netloc
        try:
            self._wait(host)
            r = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            return r.status_code
        except requests.RequestException:
            return None


# --------------------------------------------------------------------------- #
# Extraction
# --------------------------------------------------------------------------- #
def _dig(obj, path):
    for part in path.split("."):
        if isinstance(obj, list):
            obj = obj[0] if obj else None
        if not isinstance(obj, dict):
            return None
        obj = obj.get(part)
    return obj if isinstance(obj, (str, int, float)) else None


def _sel(node, spec):
    if not spec:
        return None
    sel, _, attr = spec.partition("@")
    try:
        el = node.select_one(sel) if sel else node
    except Exception:
        return None
    if el is None:
        return None
    return el.get(attr) if attr else el.get_text(" ", strip=True)


def extract(src, body, status):
    """Turn one fetched page into a list of raw dicts."""
    out = []
    if src["kind"] == "json":
        data = json.loads(body)
        for part in src["path"].split("."):
            data = data.get(part, []) if isinstance(data, dict) else data
        for rec in data or []:
            row = {k: _dig(rec, p) for k, p in src["map"].items()}
            rid = row.pop("id", None)
            row["url"] = src["link"].format(id=rid) if rid else None
            out.append(row)
    else:
        soup = BeautifulSoup(body, "lxml")
        for card in soup.select(src["card"]):
            row = {k: _sel(card, p) for k, p in src["map"].items()}
            href = _sel(card, src.get("link", "a@href"))
            if href and src.get("base"):
                href = urljoin(src["base"], href)
            row["url"] = href
            if src.get("company_default") and not row.get("company"):
                row["company"] = src["company_default"]
            if row.get("title") and row.get("url"):
                out.append(row)
    return out


def build_row(raw, src_name, today, scraped_at):
    title = (raw.get("title") or "").strip()
    blob = " ".join(str(raw.get(k) or "") for k in
                    ("title", "company", "location", "snippet", "salary")).lower()
    norm, kind = canonical_role(title)
    smin, smax, stext = parse_salary(raw.get("salary"))
    pdate, unknown = parse_date(raw.get("date"), today)
    snippet = re.sub(r"\s+", " ", str(raw.get("snippet") or "")).strip()
    company = norm_company(raw.get("company"))
    row = {
        "title": title, "title_norm": norm, "company": company,
        "company_type": company_type(raw.get("company")),
        "district": find_district(f"{raw.get('location','')} {snippet}") or "Bangkok (unspecified)",
        "posted_date": pdate, "date_unknown": unknown,
        "salary_min": smin, "salary_max": smax, "salary_text": stext,
        "experience_years": parse_experience(f"{snippet} {title}"),
        "language_of_post": detect_lang(f"{title} {snippet}"),
        "requirements_summary": snippet[:200],
        "url": raw.get("url"), "alt_urls": [], "source": src_name,
        "scraped_at": scraped_at, "_match": kind, "_blob": blob,
    }
    row["id"] = hashlib.sha1(
        f"{company}|{norm or title.lower()}|{src_name}".encode()).hexdigest()[:16]
    row["relevance_score"], row["_why"] = score(row, blob, today)
    return row


# --------------------------------------------------------------------------- #
# Collection / dedup
# --------------------------------------------------------------------------- #
def collect(http, days, today, limit_sources=None):
    rows, status = [], {}
    scraped_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for src in S.SOURCES:
        if limit_sources and src["name"] not in limit_sources:
            continue
        ok_pages = err_pages = 0
        errors, got = [], 0
        for term in src["terms"]:
            for page in range(1, src.get("pages", 1) + 1):
                url = src["url"].format(
                    kw=quote_plus(term), kw_slug=term.replace(" ", "-") or "engineering",
                    page=page, start=(page - 1) * 25, days=days, seconds=days * 86400)
                code, body, err = http.get(url)
                if code == 200 and body:
                    try:
                        found = extract(src, body, code)
                        rows.extend(build_row(r, src["name"], today, scraped_at)
                                    for r in found if r.get("title"))
                        got += len(found)
                        ok_pages += 1
                    except Exception as exc:            # parse failure, not a fetch failure
                        err_pages += 1
                        errors.append(f"parse error: {type(exc).__name__}")
                else:
                    err_pages += 1
                    errors.append(classify(err, code))
                LOG.info("%-34s %-22s -> %s", src["name"], term[:22], classify(err, code))
        if src.get("login_gated") and not got:
            state, reason = "BLOCKED", "login-gated; public URL returned no readable postings"
        elif ok_pages and not err_pages:
            state, reason = "OK", f"{got} raw listings"
        elif ok_pages and err_pages:
            state, reason = "PARTIAL", f"{got} raw listings; {_top(errors, ok_pages + err_pages)}"
        else:
            state, reason = "BLOCKED", _top(errors, err_pages)
        status[src["name"]] = {"status": state, "reason": reason, "raw": got}
    return rows, status


def classify(err, code):
    """Collapse a raw transport error into one short, readable cause."""
    if err is None:
        return f"HTTP {code}"
    if "ProxyError" in err or "Tunnel connection failed" in err:
        return "blocked by the network egress proxy (CONNECT denied)"
    if "robots.txt" in err:
        return err
    if "Timeout" in err or "timed out" in err:
        return "request timed out"
    if "SSLError" in err:
        return "TLS verification failed"
    if "ConnectionError" in err:
        return "connection refused / DNS failure"
    return err.split(":")[0]


def _top(errors, total):
    if not errors:
        return "no response"
    common = max(set(errors), key=errors.count)
    return f"{len(errors)}/{total} request(s) failed — {common}"


def title_sim(a, b):
    """Token-order-insensitive similarity, with a partial fallback for Thai titles
    (which carry no spaces, so token_sort_ratio badly understates them)."""
    a, b = a.lower(), b.lower()
    return max(fuzz.token_sort_ratio(a, b), fuzz.partial_ratio(a, b))


def dedup(rows):
    """Same company + fuzzy title >=85 -> one row; earliest posted_date wins.

    Guard: two postings whose canonical roles are both known but different
    (e.g. "Site Engineer" vs "M&E Site Engineer", which fuzz to 87) are distinct
    vacancies and must not be merged.
    """
    kept = []
    for row in sorted(rows, key=lambda r: (r["posted_date"] or datetime.max.date())):
        match = None
        for k in kept:
            if not row["company"] or not k["company"]:
                continue
            if fuzz.token_sort_ratio(row["company"].lower(), k["company"].lower()) < 90:
                continue
            if row["title_norm"] and k["title_norm"] and row["title_norm"] != k["title_norm"]:
                continue
            if title_sim(row["title"], k["title"]) >= 85:
                match = k
                break
        if match:
            if row["url"] and row["url"] not in match["alt_urls"] + [match["url"]]:
                match["alt_urls"].append(row["url"])
            if row["relevance_score"] > match["relevance_score"]:
                match["relevance_score"] = row["relevance_score"]
            if match["date_unknown"] and not row["date_unknown"]:
                match["posted_date"], match["date_unknown"] = row["posted_date"], False
        else:
            kept.append(row)
    return kept


# --------------------------------------------------------------------------- #
# Output
# --------------------------------------------------------------------------- #
def _flat(row):
    r = {k: row.get(k) for k in FIELDS}
    r["posted_date"] = row["posted_date"].isoformat() if row.get("posted_date") else ""
    r["date_unknown"] = int(bool(row.get("date_unknown")))
    r["alt_urls"] = " | ".join(row.get("alt_urls") or [])
    return r


def write_csv(path, rows, extra=()):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS + list(extra))
        w.writeheader()
        for r in rows:
            flat = _flat(r)
            flat.update({k: r.get(k, "") for k in extra})
            w.writerow(flat)


def write_sqlite(path, rows):
    con = sqlite3.connect(path)
    cols = ", ".join(f"{f} TEXT" for f in FIELDS if f != "id")
    con.execute(f"CREATE TABLE IF NOT EXISTS jobs (id TEXT PRIMARY KEY, {cols}, "
                "first_seen TEXT, last_seen TEXT)")
    for r in rows:
        flat = _flat(r)
        ph = ", ".join("?" * len(FIELDS))
        upd = ", ".join(f"{f}=excluded.{f}" for f in FIELDS if f != "id")
        con.execute(
            f"INSERT INTO jobs ({', '.join(FIELDS)}, first_seen, last_seen) "
            f"VALUES ({ph}, ?, ?) ON CONFLICT(id) DO UPDATE SET {upd}, "
            "last_seen=excluded.last_seen",
            [flat[f] for f in FIELDS] + [flat["scraped_at"], flat["scraped_at"]])
    con.commit()
    con.close()


# --------------------------------------------------------------------------- #
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--days", type=int, default=5, help="look-back window in days")
    ap.add_argument("--out", default="output", help="output directory")
    ap.add_argument("--source", action="append", help="limit to named source (repeatable)")
    ap.add_argument("--delay", type=float, default=2.0, help="seconds between hits per host")
    ap.add_argument("--no-verify", action="store_true", help="skip HTTP 200 URL verification")
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    today = datetime.now().date()
    cutoff = today - timedelta(days=args.days)
    outdir = ROOT / args.out
    outdir.mkdir(exist_ok=True)

    http = Http(delay=args.delay)
    raw, status = collect(http, args.days, today, args.source)
    args.raw_total = len(raw)

    in_window = [r for r in raw if r["date_unknown"] or
                 (r["posted_date"] and r["posted_date"] >= cutoff)]
    unique = dedup(in_window)

    kept, rejected = [], []
    for r in unique:
        if r["relevance_score"] < MIN_SCORE:
            r["reason"] = r["_why"] or f"score {r['relevance_score']} < {MIN_SCORE}"
            rejected.append(r)
        else:
            kept.append(r)

    if args.no_verify or not kept:
        verify_note = ("URL verification skipped (--no-verify)." if args.no_verify
                       else "No URLs to verify — nothing was collected.")
    else:
        bad = 0
        for r in list(kept):
            code = http.verify(r["url"])
            if code != 200:
                kept.remove(r)
                r["reason"] = f"URL did not return 200 (got {code})"
                rejected.append(r)
                bad += 1
        verify_note = (f"All {len(kept)} kept URLs re-fetched and returned HTTP 200; "
                       f"{bad} row(s) dropped for failing verification.")

    kept.sort(key=lambda r: ((r["posted_date"] or cutoff - timedelta(days=999)).toordinal(),
                             r["relevance_score"]), reverse=True)
    write_csv(outdir / "jobs.csv", kept)
    write_csv(outdir / "rejected.csv", rejected, extra=("reason",))
    write_sqlite(outdir / "jobs.sqlite", kept)
    report(outdir / "REPORT.md", kept, rejected, status, args, today, verify_note)
    (outdir / "source_status.json").write_text(json.dumps(status, indent=2, ensure_ascii=False))

    print(f"\nListings kept: {len(kept)}")
    print("\nTop 5:")
    for r in kept[:5]:
        print(f"  {r['title']} — {r['company']} — "
              f"{r['posted_date'].isoformat() if r['posted_date'] else 'unknown'} — {r['url']}")
    if not kept:
        print("  (none)")
    blocked = [n for n, s in status.items() if s["status"] == "BLOCKED"]
    print(f"\nBLOCKED sources ({len(blocked)}):")
    for n in blocked:
        print(f"  - {n}: {status[n]['reason']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
