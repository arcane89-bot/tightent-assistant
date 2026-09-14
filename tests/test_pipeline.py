"""Fixture-based tests for the parsing, scoring and dedup logic.

These fixtures are synthetic and exist ONLY to exercise the code paths — they are
never written to output/jobs.csv, which is produced solely from fetched pages.

    python -m pytest tests/ -q          (or: python tests/test_pipeline.py)
"""
import sqlite3
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import parsing as P
import run as R

TODAY = date(2026, 9, 14)


def test_relative_and_absolute_dates():
    assert P.parse_date("3 days ago", TODAY) == (date(2026, 9, 11), False)
    assert P.parse_date("2026-09-12", TODAY) == (date(2026, 9, 12), False)
    assert P.parse_date("12 Sep 2026", TODAY) == (date(2026, 9, 12), False)
    assert P.parse_date("12/09/2026", TODAY) == (date(2026, 9, 12), False)
    assert P.parse_date("Today", TODAY) == (TODAY, False)
    assert P.parse_date("2 ชั่วโมงที่แล้ว", TODAY) == (TODAY, False)      # hours -> today
    assert P.parse_date("5 วันที่แล้ว", TODAY) == (date(2026, 9, 9), False)
    assert P.parse_date("เมื่อวานนี้", TODAY) == (date(2026, 9, 13), False)
    assert P.parse_date("1 week ago", TODAY) == (date(2026, 9, 7), False)
    assert P.parse_date("", TODAY) == (None, True)                        # flagged unknown


def test_salary_and_experience():
    assert P.parse_salary("฿30,000 - ฿45,000 per month")[:2] == (30000, 45000)
    assert P.parse_salary("35,000 THB")[:2] == (35000, None)
    assert P.parse_salary("600,000 - 720,000 per year")[:2] == (50000, 60000)
    assert P.parse_salary("Negotiable")[:2] == (None, None)
    assert P.parse_salary("Negotiable")[2] == "Negotiable"                # raw kept
    assert P.parse_salary(None) == (None, None, None)
    assert P.parse_experience("At least 3 years of site experience") == 3
    assert P.parse_experience("ประสบการณ์ 5 ปี") == 5
    assert P.parse_experience("no number here") is None


def test_role_canonicalisation():
    assert P.canonical_role("Site Engineer") == ("Site Engineer", "exact")
    assert P.canonical_role("วิศวกรสนาม") == ("Site Engineer", "exact")
    assert P.canonical_role("วิศวกรโยธา") == ("Civil Site Engineer", "exact")
    assert P.canonical_role("Senior Civil Site Engineer")[0] == "Civil Site Engineer"
    assert P.canonical_role("Senior Civil Site Engineer")[1] == "partial"
    assert P.canonical_role("Site Civil Engineer")[0] == "Civil Site Engineer"
    assert P.canonical_role("Accountant") == (None, "none")


def test_company_normalisation_and_type():
    assert P.norm_company("บริษัท Italian-Thai Development จำกัด (มหาชน)") == "Italian Thai Development"
    assert P.norm_company("Ch. Karnchang Public Company Limited") == "Ch Karnchang"
    assert P.company_type("Sino-Thai Engineering & Construction PCL") == "contractor"
    assert P.company_type("Sansiri PCL") == "developer"
    assert P.company_type("Adecco Consulting Ltd.") == "agency"
    assert P.company_type("Meinhardt (Thailand)") == "consultant"


def test_district_detection():
    assert P.find_district("Khlong Toei, Bangkok") == "Khlong Toei"
    assert P.find_district("ห้วยขวาง กรุงเทพมหานคร") == "Huai Khwang"
    assert P.find_district("Samut Prakan") == "Samut Prakan"
    assert P.find_district("Bangkok") == "Bangkok (unspecified)"
    assert P.find_district("Chiang Mai") is None


def _row(**kw):
    raw = {"title": "Site Engineer", "company": "Ritta Co., Ltd.",
           "location": "Khlong Toei, Bangkok", "date": "1 day ago",
           "salary": "35,000 - 45,000 THB", "snippet": "Site-based role on a condominium project.",
           "url": "https://example.test/job/1"}
    raw.update(kw)
    return R.build_row(raw, "TestSource", TODAY, "2026-09-14T00:00:00+00:00")


def test_scoring_rules():
    # 40 exact + 20 site-based + 15 district + 10 salary + 10 fresh = 95
    assert _row()["relevance_score"] == 95
    # no district beyond "Bangkok", no salary, 4 days old -> 40 + 20 = 60
    older = _row(location="Bangkok", salary=None, date="4 days ago")
    assert older["relevance_score"] == 60
    # manager title -> -30
    assert _row(title="Senior Project Manager")["relevance_score"] < _row()["relevance_score"]
    # clearly off-scope -> dropped below the keep threshold
    sales = _row(title="Sales Engineer", snippet="Sell products to clients.")
    assert sales["relevance_score"] < R.MIN_SCORE
    # plain "Senior Site Engineer" is NOT penalised as manager-level
    assert _row(title="Senior Site Engineer")["relevance_score"] >= R.MIN_SCORE


def test_dedup_merges_and_keeps_earliest_date():
    a = _row(title="Civil Site Engineer", date="2026-09-12", url="https://a.test/1")
    b = _row(title="Site Engineer (Civil)", date="2026-09-10", url="https://b.test/2")
    b["source"] = "OtherSource"
    out = R.dedup([a, b])
    assert len(out) == 1, "near-identical titles at one company must collapse"
    assert out[0]["posted_date"] == date(2026, 9, 10), "earliest posted_date wins"
    assert "https://a.test/1" in out[0]["alt_urls"], "other URLs preserved in alt_urls"


def test_dedup_does_not_merge_distinct_roles():
    """'Site Engineer' and 'M&E Site Engineer' fuzz to 87 but are different vacancies."""
    a = _row(title="Site Engineer")
    b = _row(title="M&E Site Engineer")
    assert len(R.dedup([a, b])) == 2


def test_dedup_merges_thai_near_duplicates():
    a = _row(title="วิศวกรสนาม", url="https://a.test/1")
    b = _row(title="วิศวกรสนาม (ประจำไซต์งาน)", url="https://b.test/2")
    assert len(R.dedup([a, b])) == 1


def test_dedup_keeps_different_companies_apart():
    a = _row(company="Ritta Co., Ltd.")
    b = _row(company="Sansiri PCL")
    assert len(R.dedup([a, b])) == 2


def test_unknown_date_is_flagged_not_dropped():
    r = _row(date=None)
    assert r["date_unknown"] is True and r["posted_date"] is None


def test_thai_title_stays_thai_with_english_norm():
    r = _row(title="วิศวกรสนาม")
    assert r["title"] == "วิศวกรสนาม"          # §6: Thai text stays Thai
    assert r["title_norm"] == "Site Engineer"  # English canonical form
    assert r["language_of_post"] in ("th", "mixed")


def test_sqlite_upsert_is_idempotent():
    """Daily re-runs must append new jobs and refresh old ones, never duplicate."""
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "jobs.sqlite"
        day1 = _row()
        day2 = dict(day1, scraped_at="2026-09-15T00:00:00+00:00", relevance_score=99)
        fresh = _row(company="Sansiri PCL", url="https://example.test/job/2")
        R.write_sqlite(db, [day1])
        R.write_sqlite(db, [day2, fresh])
        con = sqlite3.connect(db)
        assert con.execute("SELECT COUNT(*) FROM jobs").fetchone()[0] == 2
        first, last = con.execute(
            "SELECT first_seen, last_seen FROM jobs WHERE id=?", (day1["id"],)).fetchone()
        assert first == "2026-09-14T00:00:00+00:00"    # first_seen preserved
        assert last == "2026-09-15T00:00:00+00:00"     # last_seen refreshed
        con.close()


def test_id_is_stable_and_source_scoped():
    assert _row()["id"] == _row()["id"]
    assert len(_row()["id"]) == 16


if __name__ == "__main__":
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except AssertionError as exc:
                fails += 1
                print(f"FAIL {name}: {exc}")
    print(f"\n{fails} failure(s)")
    sys.exit(1 if fails else 0)
