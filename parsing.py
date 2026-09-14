"""Field parsers, normalisers and the §4 relevance score.

Pure functions, no I/O — this is the module the test-suite exercises.
"""
from __future__ import annotations

import re
from datetime import datetime, timedelta

import sources as S

THAI = re.compile(r"[\u0e00-\u0e7f]")


_REL_UNITS = {"minute": 0, "hour": 0, "day": 1, "week": 7, "month": 30,
              "นาที": 0, "ชั่วโมง": 0, "วัน": 1, "สัปดาห์": 7, "เดือน": 30}
_MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}


def parse_date(text, today):
    """Return (date|None, date_unknown). Handles ISO, '3 days ago', Thai relatives."""
    if not text:
        return None, True
    t = str(text).strip().lower()
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", t)
    if m:
        return datetime(*map(int, m.groups())).date(), False
    if any(w in t for w in ("today", "just posted", "วันนี้", "ล่าสุด", "new")):
        return today, False
    if any(w in t for w in ("yesterday", "เมื่อวาน")):
        return today - timedelta(days=1), False
    m = re.search(r"(\d+)\+?\s*(minute|hour|day|week|month|นาที|ชั่วโมง|วัน|สัปดาห์|เดือน)", t)
    if m:
        return today - timedelta(days=int(m.group(1)) * _REL_UNITS[m.group(2)]), False
    m = re.search(r"(\d{1,2})\s+([a-z]{3})[a-z]*\.?\s*(\d{4})?", t)
    if m and m.group(2) in _MONTHS:
        yr = int(m.group(3)) if m.group(3) else today.year
        try:
            return datetime(yr, _MONTHS[m.group(2)], int(m.group(1))).date(), False
        except ValueError:
            pass
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", t)
    if m:
        d, mo, y = map(int, m.groups())
        try:
            return datetime(y, mo, d).date(), False
        except ValueError:
            pass
    return None, True


def parse_salary(text):
    """Return (min, max, raw) in THB/month; None when not stated."""
    if not text:
        return None, None, None
    raw = str(text).strip()
    if re.search(r"negotiab|ตามตกลง|ตามโครงสร้าง|not specified", raw, re.I):
        return None, None, raw
    nums = [int(n.replace(",", "")) for n in re.findall(r"\d[\d,]{2,}", raw)]
    nums = [n for n in nums if 5_000 <= n <= 1_000_000]
    if not nums:
        return None, None, raw
    if re.search(r"per year|/\s*year|ต่อปี|annual", raw, re.I):
        nums = [round(n / 12) for n in nums]
    return min(nums), (max(nums) if len(nums) > 1 else None), raw


def parse_experience(text):
    if not text:
        return None
    m = re.search(r"(\d{1,2})\s*(?:-|–|to|ถึง)?\s*(\d{1,2})?\s*(?:\+)?\s*"
                  r"(?:years?|yrs?|ปี)", str(text), re.I)
    if m:
        v = int(m.group(1))
        return v if 0 <= v <= 40 else None
    return None


def detect_lang(text):
    text = text or ""
    has_th = bool(THAI.search(text))
    has_en = bool(re.search(r"[A-Za-z]{3,}", text))
    return "mixed" if has_th and has_en else "th" if has_th else "en"


def norm_company(name):
    if not name:
        return ""
    n = re.sub(r"\(.*?\)", " ", str(name))
    n = re.sub(r"\b(co\.?,?\s*ltd\.?|company limited|public company limited|pcl\.?|"
               r"plc\.?|corp\.?|corporation|inc\.?|group|holdings?)\b", " ", n, flags=re.I)
    n = re.sub(r"(บริษัท|จำกัด|มหาชน|กลุ่ม|หจก\.?|บมจ\.?)", " ", n)
    return re.sub(r"[\s,\.\-]+", " ", n).strip()


def company_type(name):
    n = (name or "").lower()
    for bucket, keys in (("contractor", S.CONTRACTORS), ("developer", S.DEVELOPERS),
                         ("consultant", S.CONSULTANTS), ("agency", S.AGENCIES)):
        if any(k in n for k in keys):
            return bucket
    if re.search(r"construction|engineering|ก่อสร้าง|วิศวกรรม", n):
        return "contractor"
    if re.search(r"property|estate|development|พัฒนา", n):
        return "developer"
    return "other"


def canonical_role(title):
    """Return (title_norm, 'exact'|'partial'|'none')."""
    if not title:
        return None, "none"
    t = re.sub(r"\s+", " ", str(title)).strip()
    low = t.lower()
    for th, en in S.ROLES_TH.items():
        if th in t:
            core = re.sub(r"[^฀-๿]", "", t)
            return en, "exact" if core == th else "partial"
        for role in S.ROLES_EN:
            if low == role.lower():
                return role, "exact"
    for role in S.ROLES_EN:
        if low == role.lower():
            return role, "exact"
    for alias, canon in S.ALIASES_EN.items():
        if alias in low:
            return canon, "exact" if low == alias else "partial"
    for role in sorted(S.ROLES_EN, key=len, reverse=True):
        if role.lower() in low:
            return role, "partial"
    if re.search(r"\bsite\b.*\bengineer\b|\bengineer\b.*\bsite\b", low):
        return "Site Engineer", "partial"
    return None, "none"


def find_district(text):
    text = text or ""
    low = text.lower()
    for th, en in S.DISTRICTS_TH.items():
        if th in text:
            return en
    for d in S.BANGKOK_DISTRICTS:
        if re.search(rf"\b{re.escape(d.lower())}\b", low):
            return d
    for prov, keys in S.METRO_PROVINCES.items():
        if any(k in low for k in keys):
            return prov
    if any(h in low for h in S.BANGKOK_HINTS):
        return "Bangkok (unspecified)"
    return None


def score(row, blob, today):
    """§4 relevance score, 0-100."""
    pts, why = 0, []
    kind = row["_match"]
    pts += {"exact": 40, "partial": 25}.get(kind, 0)
    if any(h in blob for h in S.SITE_BASED_HINTS):
        pts += 20
    if row["district"] and row["district"] != "Bangkok (unspecified)":
        pts += 15
    if row["salary_min"] is not None:
        pts += 10
    if not row["date_unknown"] and row["posted_date"] and \
            (today - row["posted_date"]).days <= 2:
        pts += 10
    exp = row["experience_years"]
    if any(h in blob for h in S.SENIOR_HINTS) or (exp is not None and exp >= 10):
        pts -= 30
        why.append("senior/manager level")
    if any(h in blob for h in S.OFFSCOPE_HINTS):
        pts -= 50
        why.append("off-scope role")
    if kind == "none":
        why.append("title does not match a target role")
    return max(0, min(100, pts)), "; ".join(why)
