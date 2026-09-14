# Bangkok Site Engineer job pipeline
Collects, dedups, scores and reports Site Engineer openings in the Bangkok metro area.
Run: `pip install requests beautifulsoup4 lxml rapidfuzz && python run.py --days 5`
Outputs to `output/`: `jobs.csv`, `jobs.sqlite` (upserted by `id` — daily re-runs append, never duplicate), `rejected.csv`, `REPORT.md`.
- **Day window:** `--days N` (default 5); TODAY comes from the system clock, never hard-coded.
- **Add a source:** append a dict to `SOURCES` in `sources.py` — `kind:"json"` (walk `path`, map dot-paths) or `kind:"html"` (CSS `card` + per-field selectors, `sel@attr` for an attribute). No engine changes needed.
- **Other flags:** `--source "JobsDB Thailand"` (repeatable, test one source), `--delay` (default 2s per host), `--no-verify` (skip HTTP-200 URL checks).
- **Sprawdzenie sieci / network preflight:** `python check_net.py` — 5 s, mówi czy egress jest otwarty, zanim odpalisz pełny crawl.
- **Tests:** `python tests/test_pipeline.py` — date/salary parsing, scoring, dedup.
- **Layout:** `run.py` (fetch/dedup/export) · `parsing.py` (field parsers + score) · `sources.py` (catalog) · `reporting.py` (REPORT.md).
