"""REPORT.md builder and the run-time assumption log."""
from __future__ import annotations

import statistics
from datetime import datetime, timedelta, timezone

MIN_SCORE = 30


def report(path, kept, rejected, status, args, today, verify_note):
    n_salary = [r["salary_min"] for r in kept if r["salary_min"]]
    by_src, by_day, by_co = {}, {}, {}
    for r in kept:
        by_src[r["source"]] = by_src.get(r["source"], 0) + 1
        key = r["posted_date"].isoformat() if r["posted_date"] else "unknown"
        by_day[key] = by_day.get(key, 0) + 1
        by_co[r["company"] or "(unknown)"] = by_co.get(r["company"] or "(unknown)", 0) + 1
    n_blocked = sum(1 for v in status.values() if v["status"] == "BLOCKED")
    L = [f"# Site Engineer openings — Bangkok metro (last {args.days} days)", "",
         f"Run: {datetime.now(timezone.utc).isoformat(timespec='seconds')}  ",
         f"Window: **{(today - timedelta(days=args.days)).isoformat()} → {today.isoformat()}**", ""]
    if not kept and n_blocked == len(status):
        L += ["> ## ⚠ Run outcome: no data collected", ">",
              f"> **All {n_blocked} sources were unreachable on this run — every outbound HTTPS",
              "> request was refused by the network egress proxy before it reached the host.**",
              "> This is an environment restriction, not a finding about the Thai job market:",
              "> it says nothing about how many Site Engineer roles are actually open in Bangkok.",
              ">",
              "> Zero rows were written to `jobs.csv`. No listing, company, salary, date or URL has",
              "> been invented to fill the gap (§6). Re-run `python run.py --days 5` from a host with",
              "> outbound internet access and the same command will populate every deliverable.",
              "> See the **Source status** table below for the per-source result.", ""]
    L += ["## Headline numbers", "",
         f"- Raw listings fetched: **{args.raw_total}**",
         f"- Unique after dedup: **{len(kept) + len(rejected)}**",
         f"- Kept (score >= {MIN_SCORE}): **{len(kept)}**",
         f"- Rejected: **{len(rejected)}** (see `rejected.csv`)", ""]
    L += ["### By source", "", "| source | kept |", "|---|---|"]
    L += [f"| {k} | {v} |" for k, v in sorted(by_src.items(), key=lambda x: -x[1])] or ["| — | 0 |"]
    L += ["", "### By day", "", "| posted_date | kept |", "|---|---|"]
    L += [f"| {k} | {v} |" for k, v in sorted(by_day.items(), reverse=True)] or ["| — | 0 |"]
    L += ["", "## Top 20", "",
          "| # | title | company | district | salary | posted | link |", "|---|---|---|---|---|---|---|"]
    top = sorted(kept, key=lambda r: (-r["relevance_score"],
                                      -(r["posted_date"] or today - timedelta(days=999)).toordinal()))[:20]
    for i, r in enumerate(top, 1):
        L.append(f"| {i} | {r['title']} | {r['company']} | {r['district']} | "
                 f"{r['salary_text'] or '—'} | "
                 f"{r['posted_date'].isoformat() if r['posted_date'] else 'unknown'} | "
                 f"[link]({r['url']}) |")
    if not top:
        L.append("| — | no listings collected | | | | | |")
    L += ["", "## Salary distribution (THB/month, where stated)", ""]
    L += ([f"- min **{min(n_salary):,}** / median **{round(statistics.median(n_salary)):,}** "
           f"/ max **{max(n_salary):,}** (n={len(n_salary)})"]
          if n_salary else ["- No salaries stated in the collected set."])
    L += ["", "## Companies hiring the most", ""]
    L += [f"- {c} — {n}" for c, n in sorted(by_co.items(), key=lambda x: -x[1])[:15]] or ["- —"]
    L += ["", "## Source status", "", "| source | status | reason |", "|---|---|---|"]
    for name, st in status.items():
        L.append(f"| {name} | **{st['status']}** | {st['reason']} |")
    L += ["", "## URL verification", "", verify_note, "",
          "## Assumptions", ""] + [f"- {a}" for a in ASSUMPTIONS]
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


ASSUMPTIONS = [
    "TODAY is read from the system clock at run time (never hard-coded); the window is "
    "TODAY-N .. TODAY inclusive.",
    "Listings with no parseable date are kept with date_unknown=true and are NOT excluded "
    "by the window filter, since their age cannot be established.",
    "`id` hashes company + canonical title + the source of the *earliest* record in a "
    "duplicate group; the other sources' URLs land in alt_urls.",
    "Dedup requires company similarity >=90 as well as the specified title similarity >=85, "
    "so that two different employers advertising an identically-worded role stay separate.",
    "Dedup additionally refuses to merge two postings whose canonical roles are both known "
    "but different ('Site Engineer' vs 'M&E Site Engineer' fuzz to 87 yet are distinct jobs); "
    "Thai titles use a partial-ratio fallback because they contain no word spaces.",
    "'Senior' alone does not trigger the -30 penalty; it applies to manager/director/head "
    "titles or a stated requirement of 10+ years.",
    "Salary quoted per year is divided by 12 to reach THB/month; 'negotiable' is recorded in "
    "salary_text with null min/max.",
    "Bangkok metro = Bangkok plus Nonthaburi, Pathum Thani and Samut Prakan, as specified.",
    "The brief described an empty project folder; it actually already contained unrelated "
    "TIGHTENT documents. Those were left untouched and the pipeline was added alongside them.",
    "robots.txt is fetched per host and obeyed; a 5xx robots response is treated as "
    "disallow-all, a 404 as allow-all. Requests to one host are spaced >=2s.",
    "Facebook is attempted only via a public, non-login group URL; no credentials, no "
    "login bypass, no private groups.",
    "Source URL patterns and CSS selectors in sources.py were written from the published "
    "structure of each board but could NOT be validated against live markup on this run "
    "(no egress); expect to tune selectors on the first unblocked run.",
]
