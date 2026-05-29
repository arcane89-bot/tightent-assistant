# TIGHTENT — Product Knowledge Base
*AI assistant file. No prices. Prices are in TIGHTENT_cennik.md.*
*File version: 2.1 — structured for section-based token routing.*

---

## HOW TO USE THIS FILE (for AI routing logic)

Each section is tagged with a SECTION KEY in brackets.
The intent router in n8n loads only relevant sections per request.

Sections always loaded: CORE_RULES, CROSSSELL_MATRIX, IMAGE_LIBRARY
Sections loaded by keyword:
- [TENTS] -> tent, fold-up tent, pop-up tent, t1s, t1p, t2p, t4p, t9, h40, h40s, frame
- [INFLATABLE] -> inflatable, archway, sky tube, air dance, awning, connecting cloth, inflatable tent
- [FLAGS] -> flag, feather flag, teardrop flag, carbon flag, aluminum flag, beach flag, japan flag, back flag
- [BACKDROPS] -> backdrop, display wall, photo wall, pop up backdrop, led backdrop, light box
- [COUNTERS] -> counter, promotion counter, pop-up counter, table, chair, director chair
- [BANNERS] -> banner, roll up, x stand, a board, a banner, sky banner
- [UMBRELLAS] -> umbrella, hand umbrella, large umbrella

---

## [CORE_RULES] — Always include

TIGHTENT sells event marketing products: fold-up tents, flags, backdrops, counters, inflatables, umbrellas, banners.

Key rules for every response:
- Reply in English only
- Plain text output — no markdown, no bold, no bullet symbols
- Never invent prices or specs — only use data from TIGHTENT_cennik.md
- Never say "net price" — just say "price" or "our price"
- Mention VAT +7% only if customer explicitly asks about invoice/receipt
- Include image links from IMAGE_LIBRARY when they are relevant and helpful
- Production time: HD (DTF) is faster (a few working days). Sublimation (SUB) takes approx. 15–18 working days
- For urgent orders: recommend HD print or stock availability check instead of SUB
- Deposit: always 50% before production starts — no exceptions
- Graphic design: TIGHTENT prepares the design for free — customer must provide logo in good quality (AI / PDF / high-res PNG)
- Design must be approved by customer before production begins

---

## [TENTS] — Fold-up / Pop-up Tents

### What is a TIGHTENT fold-up tent
Aluminum or steel-frame pop-up event tent. Assembles without tools in minutes. Used at trade shows, outdoor events, promotions, and indoor/outdoor booths.

Every tent includes:
- Frame (steel or aluminum depending on model)
- Roof (Oxford PVC — waterproof fabric)
- Optional walls (full wall or half wall)
- Optional custom print (logo, full graphics on roof and walls)

All tent models are suitable for outdoor use. Model choice depends on budget and intensity of use — see MODEL SELECTION GUIDE below.

---

### Tent Models — Budget to Premium

T1S — Entry level, steel frame, thinnest walls (30x30x0.45mm main tubes). Lightest in range.
Sizes: 2x2m, 2x3m, 3x3m. Weight: 9.8–12 kg.
For: tight budget, light occasional use, indoor events.

T1P — Entry level reinforced, steel frame, thicker tubes than T1S (30x30x0.5mm).
Sizes: 2x2m, 2x3m, 3x3m. Weight: 12–15 kg.
For: moderate budget, occasional outdoor, first booth.

T2P — Mid range, steel frame (28x28x0.8mm tubes), more rigid than T1P.
Sizes: 2x2m, 2x3m, 3x3m. Weight: 12.5–16 kg.
For: regular outdoor use, local events.

T4P — Most popular model. Steel frame, heavy tubes (32x32x0.8mm). Best value for money. Default recommendation for most customers.
Sizes: 2x2m, 2x3m, 3x3m, 3x4.5m, 3x6m. Weight: 20–40 kg.
For: regular outdoor, trade shows, recurring events.
Note: When customer chooses full sublimation print (SUB), always recommend T4P or higher — premium print deserves a premium frame.

T9 — Heavy-duty steel, hexagonal frame joints (40x40x0.8mm tubes). Most rigid steel model.
Sizes: 3x3m, 3x4.5m, 3x6m, 4x4m, 4x6m, 4x8m. Weight: 24.5–55 kg.
For: large events, continuous intensive use, high wind exposure, heavy-duty outdoor.
Note: 4x4, 4x6, 4x8 — use catalog price. Confirm special pricing with manager.

H40 — Premium aluminum frame (40x40x1.0mm tubes). Significantly lighter than steel at same rigidity.
Sizes: 3x3m, 3x4.5m, 3x6m. Weight: 15.3–27.1 kg.
For: customers who value light weight + durability, frequent transport, premium quality.

H40S — Top-tier aluminum, thickest tubes (40x40x1.8mm). Heaviest aluminum model, maximum strength.
Sizes: 3x3m, 3x4.5m, 3x6m, 4x4m, 4x6m, 4x8m. Weight: 23.4–53 kg.
For: professional installations, international trade shows, permanent display points, highest-budget customers.
Note: All H40S sizes — use catalog price. Confirm special pricing with manager.

---

### Tent Sizes

2x2m — Small booth, point promotion, limited space.
2x3m — Standard booth, 1 counter + staff.
3x3m — Most popular size, comfortable single booth.
3x4.5m — Large booth, more product display space.
3x6m — Extra large booth, premium events.
4x4m / 4x6m / 4x8m — T9 and H40S only. Large installations and multi-brand setups.

---

### MODEL SELECTION GUIDE (Decision logic for AI)

Start the recommendation from T2P or T4P (mid-range). Then adjust:

Go lower (T1S / T1P) when:
- Customer has strict tight budget
- Occasional use only, mostly indoor
- Simple print or no print

Stay at T4P when:
- Regular outdoor use
- Full sublimation print ordered (default rule: premium print = T4P minimum)
- Trade show or recurring event booth

Go higher (T9) when:
- Heavy continuous outdoor use
- Large sizes (3x6m and above)
- High wind exposure expected
- Intensive setup/takedown schedule

Go premium (H40 / H40S) when:
- Customer prioritizes light weight + frequent transport
- International trade shows or permanent installations
- Top budget, no compromise on quality

---

### Print Techniques for Tents

HD (DTF — High Definition):
- Digital print on valance and selected panels
- Faster production
- Best for: logo, text, simple graphics
- Print ranges: A1 (valance only) through C3 (valance + 2 walls + 2 roof panels)
- Surcharge added to frame price

SUB 300D (Sublimation — standard):
- Full wrap print on roof and walls
- Better color vibrancy, higher durability
- Longer production time (~15–18 working days)
- Price covers frame + print together (not separate)

SUB 600D (Sublimation — premium):
- Thicker fabric (600D vs 300D), richer colors
- Surcharge on top of 300D price

SUB Roof — roof only (no walls)
SUB Wall — wall panels only (can be ordered separately)

---

### [TENT_ACCESSORIES] — Tent Add-ons

WALLS (Wall):
- Fabric side panel for tent
- Available sizes: 2m, 3m, 4.5m, 6m (match to tent side)
- Full wall: closes the side completely
- Can be ordered with or without HD/SUB print
- SUB Wall also available in 4m size (for 4x4m tent configurations)

HALF WALL (Half Wall):
- Waist-height side panel — leaves top open for airflow
- Available: 3m
- With or without print
- DO NOT confuse with Shelter — Half Wall is a side panel, Shelter is a roof extension

SHELTER (Roof Extension / Marquee Arm):
- NOT a side wall. A Shelter is an additional roof overhang extending from the tent frame.
- Made of steel profiles and polyester fabric
- Attaches directly to tent frame using plastic connectors
- Size refers to tent width compatibility: 2m Shelter fits 2m-wide tent, 3m fits 3m-wide tent
- For 3x6m tent (has center leg): can mount one Shelter per half, or two Shelters total
- Purpose: extra shaded area and rain protection beyond the tent footprint
- Sales approach: propose as upsell alongside tent — not as alternative to walls

SKY BANNER:
- A horizontal printed banner mounted to the vertical legs of a fold-up tent
- Compatible with any tent model where at least one side is 3m wide
- Mounted at any height on tent legs using clamp brackets (included)
- HD version: PVC banner material, faster + cheaper
- SUB version: polyester fabric, sublimation print — lighter, more elegant finish, folds without creasing
- Use: adds an extra advertising strip across the booth without full side walls

SANDBAG (SandBag — 4x16kg bags):
- ALWAYS recommend for outdoor use — mandatory safety item
- Stabilizes tent against wind
- Include in every outdoor tent quote automatically

CARRY BAG WITH WHEEL:
- Wheeled carry bag for the tent frame
- Sizes: 2x2/3x3, 3x3/3x4.5, 3x6
- Recommend whenever customer will transport tent regularly

BANNER FOR TABLE (200x180cm):
- Fabric banner with custom print, mounted on the table/counter frame
- Adds branding surface to the table side panels
- Sold separately, paired with Table SUB

BIG BANNER FOR TENT (300x150cm):
- Large fabric banner with custom print mounted to the tent structure
- Adds vertical branding on tent exterior
- Sold separately

---

## [INFLATABLE] — Inflatable Products

### Inflatable Tent
Fully inflatable event tent — alternative to fold-up tents. Faster setup, modern look.
Sizes: 3x3m, 4x4m, 5x5m, 6x6m. TPU tubes Φ20–30cm.
For: fast setup events, premium modern look, customers who want something different.
Note: Awning, Inflatable Wall, and Connecting Cloth are dedicated accessories for Inflatable Tent only.

### Awning (Inflatable Roof Extension):
- Inflatable front canopy extension — dedicated accessory for Inflatable Tent only
- No metal frame — fully inflatable structure, attaches to front of inflatable tent
- Custom print included in price
- Sizes: 3m, 4m, 5m, 6m
- Sales rule: ALWAYS propose Awning when customer buys or asks about Inflatable Tent — great visual impact, seamless look
- DO NOT confuse with Shelter (which is a steel marquee arm for fold-up tents)

### Inflatable Wall:
- Side wall panel for Inflatable Tent — NOT an inflatable structure itself
- Made of polyester fabric, attaches to inflatable tent tubes with zippers
- Not freestanding — requires inflatable tent frame
- Sizes: 3m, 4m, 5m, 6m
- Custom print included in price
- Propose together with Inflatable Tent when customer needs closed sides

### Connecting Cloth:
- Modular connector joining two Inflatable Tents together
- Made of polyester fabric, attaches between tent edges with zippers
- Allows expanding event space by linking multiple inflatable tents
- Sizes: 3m–6m (matching tent edge height)
- Custom print included in price
- Propose when customer needs two or more inflatable tents in one configuration

### Archway (Inflatable Arch):
- Inflatable branded arch / entrance gate
- Sizes: S (6x3m), M (8x4m), L (10x5m)
- Comes with 550W blower
- For: sports events, trade show entrances, outdoor promotions, branded gateways

### Sky Tube:
- Vertical inflatable tube with full sublimation print
- Sizes: 3m, 4m, 5m (with or without arms)
- Comes with 750W blower
- For: high-visibility branding, attracts attention from long distance

### LED Tube:
- Illuminated inflatable tube
- 250cm x Φ63cm
- Comes with 150W blower
- For: night events, illuminated branding

### Air Dance (Waving Man):
- Dancing inflatable figure with custom print
- 300cm x Φ46cm
- Comes with 750W blower (or without blower option)
- For: high traffic areas, extreme attention-grabbing promotion

### Inflatable Doll (Custom Mascot):
- Giant custom-shaped inflatable advertising figure
- Any shape: brand mascot, oversized product replica, character, logo form
- Standard heights: 2m, 3m, 4m+
- Made of polyester fabric, requires continuous electric blower (installed at base)
- Pricing: individual quote — customer must send design, sketch, or logo + desired height
- For: brand mascot promotion, product launches, large outdoor events

---

## [FLAGS] — Advertising Flags

Flags attract attention from distance — perfect complement to tent at any booth.

### Flag Types

Standard Flag (Teardrop / Feather shape):
- Classic teardrop/feather silhouette
- Sizes: S (260cm), M (300cm), L (410cm), XL (500cm)
- Single side or Double side
- Fiberglass pole
- For: most use cases, best price-to-quality ratio

Square Flag (Rectangle shape):
- Rectangular shape — more graphic surface area, better text readability
- Sizes: S (230cm), M (340cm), L (450cm)
- Single side or Double side

Carbon Flag:
- Carbon fiber pole — lighter and more flexible than fiberglass
- Sizes: S (270cm) to XXL (500cm)
- Single side or Double side
- For: frequent transport, better pole durability against breakage

Aluminum Flag:
- Aluminum pole — most durable
- Sizes: S (330cm), M (440cm), L (550cm)
- Single side or Double side
- For: permanent installations, intensive use, long-term outdoor display

Japan Flag (Giant vertical format):
- Large vertical format, different shape from standard flags
- Sizes: S (500cm), M (700cm)
- Single side or Double side
- For: very large events, visibility from long distance

Back Flag (Wearable backpack flag):
- Wearable mobile flag system carried on a person's back
- Set includes: ergonomic backpack harness, lightweight mast, flag
- Double side print included in price (1,490 THB)
- Any standard flag shape available (feather / teardrop / rectangle)
- No base needed — person is the support structure
- For: mobile promotions, directing foot traffic to booth, festivals, crowded outdoor events
- Key selling point: promoter can move exactly where people are — impossible with static flags

### Single Side vs Double Side
Single side: graphic visible from one side, reverse shows ~70% quality mirror image. Lower cost.
Double side: full graphic from both sides — for booths exposed from all angles (360° visibility). Higher cost, better effect.

### Flag Base Selection Guide

Match base to surface and conditions — always ask customer: indoor or outdoor? What floor surface?

X Base Grey (1kg) or X Base (2.5kg) — Flat hard surfaces (tiles, concrete, panels, asphalt). Best for indoor use. For outdoor: must add Water Bag on top for wind stability.

Water Bag (12L / 20L) — Used AS WEIGHT on top of X Base or Square Base for outdoor wind stability. Not a standalone base — pairs with a base.

Water Tank (15L / 25L) — Heavy standalone base, fill with water or sand. Best for outdoor stacionary display on hard surface. More stable than X Base + Water Bag combination.

Wall Base (0.8kg) — Vertical surface mounting. For permanent installation on building facades, entrance frames, pillars, shop fronts. Use when floor space is limited.

Square Base — Flat hard surfaces. Premium alternative to X Base. Looks more elegant (flat plate vs visible cross arms). Safer in crowded spaces — no protruding arms to trip over. More stable than X Base without additional weight.

Pin — Soft natural ground only: grass, soil, sand. Outdoor only. Best for festivals, beach events, sports fields. Highest stability on natural ground — screwed/pushed into ground.

Tent Connector — Attaches flag directly to tent leg, raising flag above roof line. ALWAYS propose when customer has a tent or is buying tent + flags together. Saves floor space, dramatically increases visibility.

Sales rule for flags: Always propose base together with flag. Always ask surface type. For outdoor — always recommend Water Tank or Pin depending on ground type. If customer already has tent — always propose Tent Connector.

---

## [BACKDROPS] — Display Walls / Backdrops

### Backdrop Standard (260g Polyester):
- Frame + fabric with sublimation print
- Sizes: 60x230cm to 600x300cm
- Options: fabric only (55% of price), frame only (65% of price), double side (+25%)
- For: conferences, events, photo walls, photo booths, branded backgrounds

### Backdrop W and C:
- W shape (wide) or C shape (curved) frame
- Sizes: 230x230cm or 300x230cm

### Arch Backdrop and Door Backdrop:
- Arch: arch-shaped frame, 600x300x80cm wide
- Door: door-shaped frame, 300x230x120cm wide
- For: elegant event entrances, photo opportunities

### Pop Up Backdrop:
- Spring-loaded instant setup — very fast assembly
- Sizes: 230x230cm, 300x230cm, 380x300cm
- For: frequent use, quick events, portability priority

### LED Backdrop:
- Illuminated LED panel backdrop
- Sizes: 100x100cm to 600x300cm
- Without LED panels: -35% from price
- Very high visual impact — attention-grabbing at events
- For: premium event setups, night events, luxury brand activations

### Light Box Backdrop:
- Illuminated from inside — fabric graphic lit from behind
- Sizes: 85x250cm to 600x250cm
- Premium visual effect
- For: high-end retail, premium exhibitions, luxury brand displays

### Crosssell note for backdrops:
When customer asks about backdrop — propose: Table SUB, Counter (as furniture for the booth), and Flags (to complete the full booth setup). Do NOT propose LED lights separately — the LED Backdrop is a separate product category, not an add-on light.

---

## [COUNTERS] — Counters and Tables

Counter A — Standard event counter. 132x40x90cm (H). Classic booth counter.

Counter LED — Counter with built-in LED lighting. 80x40x96cm (H). High-visibility display surface.

Counter S — Compact counter. 80x40x96cm (H).

Counter O — Small round-edge counter. 70x40x97cm (H).

Counter PP (Promotion Counter) — Counter with large banner panel: 80x30cm base + 180x80cm banner surface. Maximum branding space.

Pop-Up Counter — Spring-loaded fast-setup counter. Very fast assembly.

Table SUB — Table with full sublimation print on cover. Sizes: 1.5m and 1.8m. Often ordered together with tent for matching branded booth look.

HD Table — Same frame as Table SUB, but with HD (DTF) print instead of sublimation. Available in 1.2m, 1.5m, 1.8m. Faster production, lower cost than SUB Table.

Chair HD — Branded folding director chair with custom print. 63x46x78cm (H).

Banner For Table (200x180cm) — Printed fabric panel for table side branding. Mounted to Table SUB frame.

Big Banner For Tent (300x150cm) — Large printed fabric banner mounted to tent structure exterior.

Sales note: Counter and Table are separate product choices — customers typically choose ONE (either a counter OR a table, not both together). When customer asks about counter, probe: "Do you also need flags, a backdrop, or other booth elements?"

---

## [BANNERS] — Banners and Signs

X Stand S (160x60cm) / X Stand L (180x80cm) — Lightweight X-frame banner stand. Easy transport.

Roll Up S (160x60cm) — Standard retractable banner stand. Classic exhibition banner.
Roll Up L (200x85cm) — Large retractable banner stand.
Roll Up L Premium (200x85cm) — Premium mechanism, higher quality.

A Banner S (120x75cm) / M (200x100cm) / L (260x110cm) — Double-sided A-frame banner stand. Two graphic sides.

A Board S (150x70cm) / M (200x100cm) / L (300x100cm) — Rigid double-sided signboard. More permanent-looking than A Banner.

Sky Banner — Horizontal banner mounted to fold-up tent legs. See [TENT_ACCESSORIES] for full description.

---

## [UMBRELLAS] — Advertising Umbrellas

Umbrella 210T PG SUB:
- Standard advertising umbrella with sublimation print
- Sizes: 23" (small) and 30" (large)
- Options: single side, double side, double layer
- Quantity pricing: better price per unit at 100, 300, 500 units
- For: branded giveaways, promotional gifts, large quantity orders

HQ Umbrella 200D PU:
- Premium umbrella with PU (polyurethane waterproof) coating
- Sizes: 46" to 70"
- Accessories available: base, water tank, LED light
- For: restaurants, cafes, permanent outdoor installations, premium brand display

---

## [CARPET] — Event Carpet

Branded event carpet with full custom print.
Print: full logo / graphic / branded visual.
Sizes: 160x50cm and 200x80cm.
Minimum order for bulk discount: 100 pieces.
For: defining booth zones, highlighting a featured product, creating a branded walkway, or improving presentation under a display table, vehicle, or product stand.
Sales note: use carpet as a finishing add-on for booth setups, product launches, showroom corners, and photo areas.

---

## [CROSSSELL_MATRIX] — Always include (compact)

USE THESE RULES FOR NATURAL UPSELL — never pushy, always helpful framing.

TENT inquiry:
- Propose: 2x flags (Standard L or Carbon M), Table SUB or HD Table, Carry Bag With Wheel
- Outdoor rule: ALWAYS include SandBag — frame it as a safety item, not an upsell
- Large event / trade show: add Backdrop or Pop Up Backdrop, Counter
- Inflatable tent: ALWAYS propose Awning as must-have add-on

FLAG inquiry:
- Always propose matching base (ask surface type — see FLAG BASE SELECTION GUIDE)
- If customer has tent or buying tent: always propose Tent Connector
- 3+ flags: recommend Carbon or Aluminum for durability

BACKDROP inquiry:
- Propose: Table SUB or HD Table, Counter, Flags to complete booth
- Do NOT propose LED lights as separate add-on

COUNTER inquiry:
- Propose: Chair HD, Banner For Table, Table SUB if no table yet
- Always probe remaining booth needs: "Do you also need flags or a backdrop?"

FULL BOOTH / TRADE SHOW:
- Analyze what customer mentions, build modular set
- Standard full set: Tent + 2 Flags + Table SUB or Counter + Backdrop
- Premium set: Tent T4P/T9 + SUB print + Carbon/Aluminum Flags + Counter LED + Pop Up or LED Backdrop + SandBag + Carry Bag

---

## [IMAGE_LIBRARY] — Product Image URLs

Include relevant image URLs in responses when discussing these product categories.

TENTS:
- Typical printed tent booth: https://tightent.shop/wp-content/uploads/2026/02/tent_3x35.jpg
- Large tent setup: https://tightent.shop/wp-content/uploads/2026/02/tent_3x63.jpg
- Large premium tent setup: https://tightent.shop/wp-content/uploads/2026/02/tent_3x63.jpg

FLAGS:
- Flag at booth: https://tightent.shop/wp-content/uploads/2026/02/setb_5.jpg
- Flag close-up: https://tightent.shop/wp-content/uploads/2026/02/flagb_3.jpg

BACKDROPS:
- Backdrop at event: https://tightent.shop/wp-content/uploads/2026/02/backdropb_1.jpg
- Backdrop standard: https://tightent.shop/wp-content/uploads/2026/02/backdrop_1.jpg
- Backdrop set: https://tightent.shop/wp-content/uploads/2026/02/2-Set-Backdrop.jpg
- Backdrop LED: https://tightent.shop/wp-content/uploads/2024/06/AWBack-drop-LED-tightent_Backdrop-main-scaled-e1725901952753.jpg

COUNTERS AND TABLES:
- Table SUB at booth: https://tightent.shop/wp-content/uploads/2026/02/setb_4.jpg
- Table in set: https://tightent.shop/wp-content/uploads/2026/02/setb_14.jpg
- Counter top: https://tightent.shop/wp-content/uploads/2026/03/counter_top1.jpg
- Counter at event: https://tightent.shop/wp-content/uploads/2026/02/counter_1.jpg
- Counter LED: https://tightent.shop/wp-content/uploads/2026/04/22.jpg
- Promotion counter: https://tightent.shop/wp-content/uploads/2023/03/counter-ชงชิม1-scaled.jpg
- Pop-up counter: https://tightent.shop/wp-content/uploads/2023/03/TT_Pop-Up-Counter-main-scaled.jpg

FULL BOOTH SETS:
- Event set (tent + flags): https://tightent.shop/wp-content/uploads/2026/02/setb_6.jpg
- Flag set overview: https://tightent.shop/wp-content/uploads/2026/02/2-Set-Flag.jpg
- Indoor exhibition booth: https://tightent.shop/wp-content/uploads/2026/01/exhibition_booth1.jpg

INFLATABLES:
- Archway: https://tightent.shop/wp-content/uploads/2026/05/archway2-1.jpg
- Archway at event: https://tightent.shop/wp-content/uploads/2026/05/archway4-1.jpg
- Inflatable Tent: https://tightent.shop/wp-content/uploads/2026/02/inflatable_11.jpg
- Sky Tube: https://tightent.shop/wp-content/uploads/2026/02/inflatable_13.jpg
- Air Dance: https://tightent.shop/wp-content/uploads/2026/02/inflatable_7.jpg
- Sky Tube LED: https://tightent.shop/wp-content/uploads/2025/08/product_skytube-LED-scaled.jpg
- Inflatable Doll: https://tightent.shop/wp-content/uploads/2025/08/product_inflatable-doll-scaled.jpg
- Inflatable Doll 2: https://tightent.shop/wp-content/uploads/2025/04/main-scaled.jpg

BANNERS AND SIGNS:
- A Banner: https://tightent.shop/wp-content/uploads/2026/02/abanner_2.jpg
- A Banner at event: https://tightent.shop/wp-content/uploads/2026/02/abanner_3.jpg
- A Board: https://tightent.shop/wp-content/uploads/2022/08/aboardmain.jpg
- A Board menu: https://tightent.shop/wp-content/uploads/2022/08/aboardmenufav.jpg

UMBRELLAS:
- Hand umbrella: https://tightent.shop/wp-content/uploads/2026/02/1-Cover.jpg
- Hand umbrella 2: https://tightent.shop/wp-content/uploads/2026/02/umb6-1.jpg
- Large umbrella: https://tightent.shop/wp-content/uploads/2026/02/umbrella_3.jpg
- Large umbrella 2: https://tightent.shop/wp-content/uploads/2026/02/umbrella_2.jpg

CHAIRS:
- Director chair: https://tightent.shop/wp-content/uploads/2022/09/dirc1.jpg
- Chair at event: https://tightent.shop/wp-content/uploads/2022/09/chair3-scaled.jpg

CARPET:
- Carpet product: https://tightent.shop/wp-content/uploads/2026/02/carpet_1.jpg

---

## KNOWN ISSUES LOG (for file maintainer)

- Shelter vs Half Wall: FIXED in v2.0. Shelter = roof overhang extension. Half Wall = waist-height side panel. Do not confuse.
- SUB Wall 4m: confirmed as available product for 4x4m tent configurations. Added to file.
- T9 (4x4, 4x6, 4x8) and H40S (all sizes): use catalog price and confirm special pricing with manager before quoting.
- T9 (4x4, 4x6, 4x8) and H40S (all sizes): no direct selling price in the standard workflow. Use catalog price and confirm with manager before quoting.
- Inflatable Tent sizes: 3x3m, 4x4m, 5x5m, 6x6m only — no other sizes.
- Counter and Table are separate choices — customers pick one, not both together.
- Awning = inflatable-only accessory. Shelter = fold-up tent only. Do not mix.
- HD Table: same frame as Table SUB, HD print instead of sublimation. Faster production, lower price.
- Back Flag: wearable backpack flag — completely different product from standard ground flags.
