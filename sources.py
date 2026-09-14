"""Declarative source catalog for the Bangkok Site Engineer job pipeline.

Add a source by appending a dict to SOURCES. Two adapter kinds exist:
  "json"  -> fetch `url` (params formatted with {kw}/{page}/{days}), walk `path`
             to the list of records, map fields with `map` (dot paths).
  "html"  -> fetch `url`, select `card` elements, pull fields with CSS selectors.
Field selectors may be "sel" or "sel@attr" (attribute instead of text).
"""

# --- role vocabulary (see README / REPORT assumptions) -----------------------
ROLES_EN = [
    "Site Engineer", "Civil Site Engineer", "Construction Site Engineer",
    "M&E Site Engineer", "Field Engineer", "Project Engineer", "Site Supervisor",
]
# Thai role term -> English canonical form used in `title_norm`
ROLES_TH = {
    "วิศวกรสนาม": "Site Engineer",
    "วิศวกรไซต์งาน": "Site Engineer",
    "วิศวกรไซต์": "Site Engineer",
    "วิศวกรโยธา": "Civil Site Engineer",
    "วิศวกรโครงการ": "Project Engineer",
    "วิศวกรควบคุมงาน": "Site Supervisor",
    "วิศวกรงานระบบ": "M&E Site Engineer",
}
# extra English surface forms -> canonical
ALIASES_EN = {
    "site civil engineer": "Civil Site Engineer",
    "civil engineer (site)": "Civil Site Engineer",
    "mep site engineer": "M&E Site Engineer",
    "m&e engineer": "M&E Site Engineer",
    "mep engineer": "M&E Site Engineer",
    "site engineer (civil)": "Civil Site Engineer",
    "construction engineer": "Construction Site Engineer",
    "field engineer": "Field Engineer",
    "site supervisor": "Site Supervisor",
}

SEARCH_TERMS = [
    "site engineer", "civil site engineer", "construction site engineer",
    "m&e site engineer", "field engineer", "project engineer", "site supervisor",
    "วิศวกรสนาม", "วิศวกรโยธา", "วิศวกรโครงการ", "วิศวกรควบคุมงาน", "วิศวกรไซต์งาน",
]

# --- geography ---------------------------------------------------------------
BANGKOK_DISTRICTS = [
    "Phra Nakhon", "Dusit", "Nong Chok", "Bang Rak", "Bang Khen", "Bang Kapi",
    "Pathum Wan", "Pom Prap Sattru Phai", "Phra Khanong", "Min Buri", "Lat Krabang",
    "Yan Nawa", "Samphanthawong", "Phaya Thai", "Thon Buri", "Bangkok Yai",
    "Huai Khwang", "Khlong San", "Taling Chan", "Bangkok Noi", "Bang Khun Thian",
    "Phasi Charoen", "Nong Khaem", "Rat Burana", "Bang Phlat", "Din Daeng",
    "Bueng Kum", "Sathon", "Bang Sue", "Chatuchak", "Bang Kho Laem", "Prawet",
    "Khlong Toei", "Suan Luang", "Chom Thong", "Don Mueang", "Ratchathewi",
    "Lat Phrao", "Watthana", "Bang Khae", "Lak Si", "Sai Mai", "Khan Na Yao",
    "Saphan Sung", "Wang Thonglang", "Khlong Sam Wa", "Bang Na", "Thawi Watthana",
    "Thung Khru", "Bang Bon",
]
DISTRICTS_TH = {
    "พระนคร": "Phra Nakhon", "ดุสิต": "Dusit", "บางรัก": "Bang Rak",
    "บางกะปิ": "Bang Kapi", "ปทุมวัน": "Pathum Wan", "พญาไท": "Phaya Thai",
    "ห้วยขวาง": "Huai Khwang", "สาทร": "Sathon", "จตุจักร": "Chatuchak",
    "คลองเตย": "Khlong Toei", "ราชเทวี": "Ratchathewi", "ลาดพร้าว": "Lat Phrao",
    "วัฒนา": "Watthana", "บางนา": "Bang Na", "ดินแดง": "Din Daeng",
    "ประเวศ": "Prawet", "บางซื่อ": "Bang Sue", "ลาดกระบัง": "Lat Krabang",
    "สวนหลวง": "Suan Luang", "ธนบุรี": "Thon Buri", "หลักสี่": "Lak Si",
    "ดอนเมือง": "Don Mueang", "บึงกุ่ม": "Bueng Kum", "สายไหม": "Sai Mai",
}
METRO_PROVINCES = {
    "Nonthaburi": ["nonthaburi", "นนทบุรี"],
    "Pathum Thani": ["pathum thani", "pathumthani", "ปทุมธานี"],
    "Samut Prakan": ["samut prakan", "samutprakan", "สมุทรปราการ"],
}
BANGKOK_HINTS = ["bangkok", "krung thep", "กรุงเทพ", "bkk"]

# --- scoring vocabulary ------------------------------------------------------
SITE_BASED_HINTS = [
    "site-based", "site based", "on site", "on-site", "construction site",
    "at site", "site work", "field work", "project site", "หน้างาน", "ไซต์งาน",
    "ประจำไซต์", "ประจำหน่วยงาน", "คุมงาน", "ควบคุมงานก่อสร้าง",
]
SENIOR_HINTS = [
    "senior project manager", "project manager", "site manager", "construction manager",
    "general manager", "deputy manager", "department manager", "head of", "director",
    "chief", "vice president", "ผู้จัดการโครงการ", "ผู้จัดการ", "ผู้อำนวยการ",
]
OFFSCOPE_HINTS = [
    "sales engineer", "pre-sales", "presales", "software", "developer", "programmer",
    "devops", "site reliability", "data engineer", "network engineer", "system engineer",
    "application engineer", "solution engineer", "test engineer", "automation test",
    "web", "frontend", "backend", "full stack", "it support", "design engineer",
    "product engineer", "r&d engineer", "marketing", "accountant", "วิศวกรขาย",
    "โปรแกรมเมอร์", "นักพัฒนา",
]

# --- company classification --------------------------------------------------
CONTRACTORS = [
    "italian-thai development", "italian thai development", "ch. karnchang", "ch karnchang",
    "sino-thai engineering", "sino thai engineering", "nawarat patanakarn",
    "christiani & nielsen", "christiani and nielsen", "ritta", "bouygues-thai",
    "bouygues thai", "pre-built", "prebuilt", "syntec", "unique engineering",
    "powerline engineering", "ttcl", "thai obayashi", "nishimatsu", "kajima",
    "takenaka", "stecon", "seafco", "pylon", "right tunnelling", "vichitbhan",
]
DEVELOPERS = [
    "sansiri", "ap thailand", "ap (thailand)", "ananda", "origin property", "supalai",
    "land and houses", "land & houses", "sc asset", "frasers property", "pruksa",
    "quality houses", "noble development", "raimon land", "singha estate",
    "central pattana", "mqdc", "magnolia", "lpn development", "britania",
]
CONSULTANTS = [
    "meinhardt", "aecom", "arup", "jacobs", "wsp", "atkins", "team consulting",
    "epsilon", "asdecon", "pcbk", "index international", "consultant",
]
AGENCIES = [
    "adecco", "manpower", "robert walters", "michael page", "hays", "jac recruitment",
    "reeracoen", "persolkelly", "randstad", "kelly services", "recruitment", "consulting group",
]

# --- source catalog ----------------------------------------------------------
_UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
       "Chrome/128.0.0.0 Safari/537.36")

SOURCES = [
    {
        "name": "JobsDB Thailand", "kind": "json", "terms": SEARCH_TERMS, "pages": 2,
        "url": ("https://th.jobsdb.com/api/jobsearch/v5/search?siteKey=TH-Main"
                "&sourcesystem=houston&keywords={kw}&where=Bangkok&page={page}"
                "&pageSize=30&sortmode=ListedDate&locale=th-TH"),
        "path": "data",
        "map": {"title": "title", "company": "advertiser.description",
                "location": "jobLocation.label", "date": "listingDate",
                "salary": "salaryLabel", "snippet": "teaser", "id": "id"},
        "link": "https://th.jobsdb.com/job/{id}",
    },
    {
        "name": "JobThai", "kind": "html", "terms": SEARCH_TERMS, "pages": 1,
        "url": "https://www.jobthai.com/en/jobs?keyword={kw}&province=1",
        "card": "div.job-tile, div[class*=JobTile], article",
        "map": {"title": "h2, h3, a[href*='/job/']", "company": "[class*=company]",
                "location": "[class*=location]", "date": "[class*=date], time",
                "salary": "[class*=salary]", "snippet": "p"},
        "link": "a[href*='/job/']@href", "base": "https://www.jobthai.com",
    },
    {
        "name": "JobBKK", "kind": "html", "terms": SEARCH_TERMS, "pages": 1,
        "url": "https://www.jobbkk.com/jobs/list?keyword={kw}&province=%E0%B8%81%E0%B8%A3%E0%B8%B8%E0%B8%87%E0%B9%80%E0%B8%97%E0%B8%9E%E0%B8%A1%E0%B8%AB%E0%B8%B2%E0%B8%99%E0%B8%84%E0%B8%A3",
        "card": "div.box-list, div[class*=job-list] li, article",
        "map": {"title": "a[href*='/jobs/']", "company": "[class*=company]",
                "location": "[class*=location], [class*=province]",
                "date": "[class*=date], time", "salary": "[class*=salary]", "snippet": "p"},
        "link": "a[href*='/jobs/']@href", "base": "https://www.jobbkk.com",
    },
    {
        "name": "Indeed Thailand", "kind": "html", "terms": SEARCH_TERMS, "pages": 1,
        "url": "https://th.indeed.com/jobs?q={kw}&l=Bangkok&fromage={days}&sort=date",
        "card": "div.job_seen_beacon, td.resultContent",
        "map": {"title": "h2.jobTitle span", "company": "[data-testid=company-name]",
                "location": "[data-testid=text-location]", "date": "[data-testid=myJobsStateDate], span.date",
                "salary": "[class*=salary-snippet], .metadata.salary-snippet-container",
                "snippet": "[class*=job-snippet]"},
        "link": "h2.jobTitle a@href", "base": "https://th.indeed.com",
    },
    {
        "name": "LinkedIn Jobs (public)", "kind": "html", "terms": SEARCH_TERMS, "pages": 1,
        "url": ("https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
                "?keywords={kw}&location=Bangkok%2C%20Thailand&f_TPR=r{seconds}&start={start}"),
        "card": "li, div.base-card",
        "map": {"title": "h3.base-search-card__title", "company": "h4.base-search-card__subtitle",
                "location": "span.job-search-card__location",
                "date": "time@datetime", "salary": "span.job-search-card__salary-info",
                "snippet": "p"},
        "link": "a.base-card__full-link@href",
    },
    {
        "name": "Glassdoor Thailand", "kind": "html", "terms": SEARCH_TERMS[:4], "pages": 1,
        "url": "https://www.glassdoor.com/Job/bangkok-{kw_slug}-jobs-SRCH_IL.0,7_IC1150752_KO8,30.htm",
        "card": "li.JobsList_jobListItem__wjTHv, li[data-test=jobListing]",
        "map": {"title": "a[data-test=job-title]", "company": "[class*=EmployerProfile_compactEmployerName]",
                "location": "[data-test=emp-location]", "date": "[data-test=job-age]",
                "salary": "[data-test=detailSalary]", "snippet": "div[class*=descSnippet]"},
        "link": "a[data-test=job-title]@href", "base": "https://www.glassdoor.com",
    },
    {
        "name": "JobTopGun", "kind": "html", "terms": SEARCH_TERMS, "pages": 1,
        "url": "https://www.jobtopgun.com/en/jobs?keyword={kw}&location=Bangkok",
        "card": "div[class*=job-card], div[class*=JobCard], article",
        "map": {"title": "h2, h3, a[href*='/job']", "company": "[class*=company]",
                "location": "[class*=location]", "date": "[class*=date], time",
                "salary": "[class*=salary]", "snippet": "p"},
        "link": "a[href*='/job']@href", "base": "https://www.jobtopgun.com",
    },
]

# Boards discovered during research that were not named in the brief (§2.9 "plus any
# others you discover"). jobth.com in particular surfaces individual Thai-language
# site-engineer postings that the larger aggregators bury behind JS.
SOURCES += [
    {"name": "JobTH", "kind": "html", "terms": SEARCH_TERMS, "pages": 1,
     "url": "https://www.jobth.com/search.php?keyword={kw}&province=1",
     "card": "div[class*=job], tr[class*=job], li",
     "map": {"title": "a[href*='/งาน/'], a[href*='.html']", "company": "[class*=company]",
             "location": "[class*=location], [class*=province]",
             "date": "[class*=date], [class*=update]", "salary": "[class*=salary]", "snippet": "p"},
     "link": "a[href*='.html']@href", "base": "https://www.jobth.com"},
    {"name": "JobThaiWeb", "kind": "html", "terms": SEARCH_TERMS, "pages": 1,
     "url": "https://www.jobthaiweb.com/joblist.php?keyword={kw}",
     "card": "div[class*=job], tr, li",
     "map": {"title": "a[href*='jobdetail']", "company": "[class*=company]",
             "location": "[class*=location]", "date": "[class*=date]",
             "salary": "[class*=salary]", "snippet": "p"},
     "link": "a[href*='jobdetail']@href", "base": "https://www.jobthaiweb.com"},
    {"name": "JobMyWay", "kind": "html", "terms": SEARCH_TERMS[:7], "pages": 1,
     "url": "https://www.jobmyway.com/job-search?keyword={kw}",
     "card": "div[class*=job-card], div[class*=jobitem], li",
     "map": {"title": "a[href*='jobdescription']", "company": "[class*=company]",
             "location": "[class*=location]", "date": "[class*=date]",
             "salary": "[class*=salary]", "snippet": "p"},
     "link": "a[href*='jobdescription']@href", "base": "https://www.jobmyway.com"},
]

# Agency boards (§2.8) and employer career pages (§2.9) share the generic HTML adapter.
_GENERIC_MAP = {
    "title": "h2, h3, a", "company": "[class*=company], [class*=employer]",
    "location": "[class*=location], [class*=region]", "date": "[class*=date], time",
    "salary": "[class*=salary]", "snippet": "p",
}
_GENERIC_CARD = ("li[class*=job], div[class*=job-card], div[class*=JobCard], "
                 "div[class*=job-result], article, tr[class*=job]")

_AGENCY_BOARDS = [
    ("Adecco Thailand", "https://adecco.co.th/en/job-search?keyword={kw}", "https://adecco.co.th"),
    ("Manpower Thailand", "https://www.manpowerthailand.com/en/jobs?search={kw}", "https://www.manpowerthailand.com"),
    ("Robert Walters Thailand", "https://www.robertwalters.co.th/jobs.html?searchTerm={kw}", "https://www.robertwalters.co.th"),
    ("Michael Page Thailand", "https://www.michaelpage.co.th/jobs/{kw_slug}", "https://www.michaelpage.co.th"),
    ("Hays Thailand", "https://www.hays.co.th/job-search/{kw_slug}", "https://www.hays.co.th"),
]

_CAREER_PAGES = [
    ("Italian-Thai Development", "https://www.itd.co.th/career/", "https://www.itd.co.th"),
    ("Ch. Karnchang", "https://www.ck.co.th/career", "https://www.ck.co.th"),
    ("Sino-Thai Engineering", "https://www.stecon.co.th/en/career", "https://www.stecon.co.th"),
    ("Nawarat Patanakarn", "https://www.nawarat.co.th/career", "https://www.nawarat.co.th"),
    ("Christiani & Nielsen", "https://www.cn-thai.co.th/careers", "https://www.cn-thai.co.th"),
    ("Ritta", "https://www.ritta.co.th/career", "https://www.ritta.co.th"),
    ("Bouygues-Thai", "https://www.bouygues-thai.com/careers", "https://www.bouygues-thai.com"),
    ("Pre-Built", "https://www.prebuilt.co.th/career", "https://www.prebuilt.co.th"),
    ("Sansiri", "https://careers.sansiri.com/jobs", "https://careers.sansiri.com"),
    ("AP Thailand", "https://www.apthai.com/en/career", "https://www.apthai.com"),
    ("Ananda Development", "https://ananda.co.th/en/careers", "https://ananda.co.th"),
    ("Origin Property", "https://origin.co.th/career", "https://origin.co.th"),
    ("Supalai", "https://www.supalai.com/career", "https://www.supalai.com"),
    ("Land & Houses", "https://lh.co.th/th/career", "https://lh.co.th"),
    ("SC Asset", "https://www.scasset.com/career/", "https://www.scasset.com"),
    ("Frasers Property Thailand", "https://frasersproperty.co.th/careers", "https://frasersproperty.co.th"),
]

for _n, _u, _b in _AGENCY_BOARDS:
    SOURCES.append({"name": _n, "kind": "html", "terms": SEARCH_TERMS[:4], "pages": 1,
                    "url": _u, "card": _GENERIC_CARD, "map": dict(_GENERIC_MAP),
                    "link": "a@href", "base": _b, "company_default": _n})
for _n, _u, _b in _CAREER_PAGES:
    SOURCES.append({"name": f"Career page: {_n}", "kind": "html", "terms": [""], "pages": 1,
                    "url": _u, "card": _GENERIC_CARD, "map": dict(_GENERIC_MAP),
                    "link": "a@href", "base": _b, "company_default": _n})

# §2.10 public, non-login Facebook URLs only. Never authenticated, never private groups.
SOURCES.append({
    "name": "Facebook public groups", "kind": "html", "terms": [""], "pages": 1,
    "url": "https://www.facebook.com/groups/engineerjobthailand/",
    "card": "div[role=article]", "map": dict(_GENERIC_MAP), "link": "a@href",
    "base": "https://www.facebook.com", "login_gated": True,
})

# §2.11 catch-all: site-restricted Google queries (HTML endpoint, no API key).
SOURCES.append({
    "name": "Google site-restricted search", "kind": "html", "terms": SEARCH_TERMS, "pages": 1,
    "url": "https://www.google.com/search?q={kw}+%E0%B8%81%E0%B8%A3%E0%B8%B8%E0%B8%87%E0%B9%80%E0%B8%97%E0%B8%9E+site%3Ath.jobsdb.com+OR+site%3Ajobthai.com+OR+site%3Ajobbkk.com&tbs=qdr:{days}d",
    "card": "div.g, div[data-hveid]",
    "map": {"title": "h3", "company": "cite", "location": "span", "date": "span.f",
            "salary": "", "snippet": "div[data-sncf], span"},
    "link": "a@href",
})

HEADERS = {"User-Agent": _UA, "Accept-Language": "th,en;q=0.9",
           "Accept": "text/html,application/json;q=0.9,*/*;q=0.8"}
