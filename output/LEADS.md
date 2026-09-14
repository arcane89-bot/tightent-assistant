# Unverified leads (NOT the deliverable)

`leads.csv` holds individual job-posting URLs discovered through `WebSearch`, the only
network channel reachable from this environment. **These are leads, not listings.**

What is real: the URL and the title string, exactly as the search index returned them.

What is NOT established, and must not be assumed:
- **posted_date — completely unknown.** Nothing here is confirmed to be within the last
  5 days, or within the last 5 years. Search-index entries carry stale labels
  (the same result set mixed "Sep 2025", "May 2026" and "Jul 2026").
- company, district, salary, requirements — the pages could not be fetched. Where the
  `notes` column repeats a district or salary, that is an unverified claim from a search
  summary, not a value read off the posting.
- HTTP 200 — no URL here has been verified.

This is why these rows are in `leads.csv` and **not** in `jobs.csv`: §6 requires every row
to come from a page actually fetched, with a verified URL. Feeding them into the master
table would mean inventing dates, which is exactly what the brief forbids.

To turn leads into real rows: run `python run.py --days 5` from a host with internet
access. jobth.com, jobthaiweb.com and jobmyway.com are now in `sources.py`.
