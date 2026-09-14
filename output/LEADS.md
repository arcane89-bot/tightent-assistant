# Unverified leads (NOT the deliverable)

`leads.csv` holds 26 individual job-posting URLs discovered through `WebSearch` — the only
network channel reachable from this environment. **These are leads, not listings.**

| | |
|---|---|
| by board | jobth.com 16 · jobbkk.com 8 · jobthaiweb.com 1 · jobmyway.com 1 |
| by role | Site Engineer 10 · Civil Site Engineer 8 · Project Engineer 4 · M&E Site Engineer 2 · Site Supervisor 2 |
| employer named in the title | 9 (incl. Pre-Built PCL ×2, Jardine Engineering, C.E.S., WEL Grade Engineering PCL, Landy Home) |

**What is real:** the URL, the title string, and — where jobbkk.com puts it in the title —
the employer name. Those came back verbatim from the search index.

**What is NOT established:**
- **posted_date — completely unknown.** Nothing here is confirmed to be within the last
  5 days, or the last 5 years. Search-index entries carried stale, contradictory labels
  ("Aug 2025", "Feb 2026", "Jul 2026") in a single result set. One lead
  (`jobbkk.com/jobs/detail/7342/885700`) was described as last updated 2026-08-28, which
  would put it *outside* a 5-day window entirely — a good illustration of the problem.
- **district / salary** — everything in `unverified_claims` is a second-hand assertion from
  a search summary, not a value read off the posting. Treat it as a hint for triage, nothing more.
- **HTTP 200** — not one URL here has been verified. Some may be expired or dead.

This is precisely why these rows sit in `leads.csv` and **not** in `jobs.csv`: §6 requires
every row to come from a page actually fetched, with a verified URL. Promoting them would
mean inventing posting dates — the one thing the brief rules out.

**To convert leads into real rows:** run `python check_net.py`, then `python run.py --days 5`
from a host with outbound internet. jobth.com, jobthaiweb.com and jobmyway.com are already
registered in `sources.py`; jobbkk.com was in the brief. The pipeline will fetch each posting,
read the real date, verify the URL and score it.
