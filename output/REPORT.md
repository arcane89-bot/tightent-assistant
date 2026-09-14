# Site Engineer openings — Bangkok metro (last 5 days)

Run: 2026-09-14T12:55:30+00:00  
Window: **2026-09-09 → 2026-09-14**

> ## ⚠ Run outcome: no data collected
>
> **All 30 sources were unreachable on this run — every outbound HTTPS
> request was refused by the network egress proxy before it reached the host.**
> This is an environment restriction, not a finding about the Thai job market:
> it says nothing about how many Site Engineer roles are actually open in Bangkok.
>
> Zero rows were written to `jobs.csv`. No listing, company, salary, date or URL has
> been invented to fill the gap (§6). Re-run `python run.py --days 5` from a host with
> outbound internet access and the same command will populate every deliverable.
> See the **Source status** table below for the per-source result.

## Headline numbers

- Raw listings fetched: **0**
- Unique after dedup: **0**
- Kept (score >= 30): **0**
- Rejected: **0** (see `rejected.csv`)

### By source

| source | kept |
|---|---|
| — | 0 |

### By day

| posted_date | kept |
|---|---|
| — | 0 |

## Top 20

| # | title | company | district | salary | posted | link |
|---|---|---|---|---|---|---|
| — | no listings collected | | | | | |

## Salary distribution (THB/month, where stated)

- No salaries stated in the collected set.

## Companies hiring the most

- —

## Source status

| source | status | reason |
|---|---|---|
| JobsDB Thailand | **BLOCKED** | 24/24 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| JobThai | **BLOCKED** | 12/12 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| JobBKK | **BLOCKED** | 12/12 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Indeed Thailand | **BLOCKED** | 12/12 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| LinkedIn Jobs (public) | **BLOCKED** | 12/12 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Glassdoor Thailand | **BLOCKED** | 4/4 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| JobTopGun | **BLOCKED** | 12/12 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Adecco Thailand | **BLOCKED** | 4/4 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Manpower Thailand | **BLOCKED** | 4/4 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Robert Walters Thailand | **BLOCKED** | 4/4 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Michael Page Thailand | **BLOCKED** | 4/4 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Hays Thailand | **BLOCKED** | 4/4 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Career page: Italian-Thai Development | **BLOCKED** | 1/1 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Career page: Ch. Karnchang | **BLOCKED** | 1/1 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Career page: Sino-Thai Engineering | **BLOCKED** | 1/1 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Career page: Nawarat Patanakarn | **BLOCKED** | 1/1 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Career page: Christiani & Nielsen | **BLOCKED** | 1/1 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Career page: Ritta | **BLOCKED** | 1/1 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Career page: Bouygues-Thai | **BLOCKED** | 1/1 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Career page: Pre-Built | **BLOCKED** | 1/1 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Career page: Sansiri | **BLOCKED** | 1/1 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Career page: AP Thailand | **BLOCKED** | 1/1 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Career page: Ananda Development | **BLOCKED** | 1/1 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Career page: Origin Property | **BLOCKED** | 1/1 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Career page: Supalai | **BLOCKED** | 1/1 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Career page: Land & Houses | **BLOCKED** | 1/1 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Career page: SC Asset | **BLOCKED** | 1/1 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Career page: Frasers Property Thailand | **BLOCKED** | 1/1 request(s) failed — blocked by the network egress proxy (CONNECT denied) |
| Facebook public groups | **BLOCKED** | login-gated; public URL returned no readable postings |
| Google site-restricted search | **BLOCKED** | 12/12 request(s) failed — blocked by the network egress proxy (CONNECT denied) |

## URL verification

No URLs to verify — nothing was collected.

## Assumptions

- TODAY is read from the system clock at run time (never hard-coded); the window is TODAY-N .. TODAY inclusive.
- Listings with no parseable date are kept with date_unknown=true and are NOT excluded by the window filter, since their age cannot be established.
- `id` hashes company + canonical title + the source of the *earliest* record in a duplicate group; the other sources' URLs land in alt_urls.
- Dedup requires company similarity >=90 as well as the specified title similarity >=85, so that two different employers advertising an identically-worded role stay separate.
- Dedup additionally refuses to merge two postings whose canonical roles are both known but different ('Site Engineer' vs 'M&E Site Engineer' fuzz to 87 yet are distinct jobs); Thai titles use a partial-ratio fallback because they contain no word spaces.
- 'Senior' alone does not trigger the -30 penalty; it applies to manager/director/head titles or a stated requirement of 10+ years.
- Salary quoted per year is divided by 12 to reach THB/month; 'negotiable' is recorded in salary_text with null min/max.
- Bangkok metro = Bangkok plus Nonthaburi, Pathum Thani and Samut Prakan, as specified.
- The brief described an empty project folder; it actually already contained unrelated TIGHTENT documents. Those were left untouched and the pipeline was added alongside them.
- robots.txt is fetched per host and obeyed; a 5xx robots response is treated as disallow-all, a 404 as allow-all. Requests to one host are spaced >=2s.
- Facebook is attempted only via a public, non-login group URL; no credentials, no login bypass, no private groups.
- Source URL patterns and CSS selectors in sources.py were written from the published structure of each board but could NOT be validated against live markup on this run (no egress); expect to tune selectors on the first unblocked run.
