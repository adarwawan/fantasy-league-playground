# 10 — Bonus Distribution per Team (2025/26 retrospective)

Bonus points (the BPS podium — 3/2/1 per match) are noisy game-by-game but tell a real story
over a season. This notebook attributes every bonus point the 2025/26 season handed out to a
**team**, then drills down **by position** and **by player**.

- **Notebooks:** [bonus_distribution.ipynb](bonus_distribution.ipynb) (2025/26, vaastav CSV) and
  [bonus_distribution_26.ipynb](bonus_distribution_26.ipynb) (2026/27 season-to-date, official FPL API:
  `bootstrap-static` + `event/{gw}/live`; in-progress GW is provisional).
- **Data:** vaastav `2025-26/gws/merged_gw.csv` only — raw per-GW `bonus` counts, no fixtures.
- **Split is lossless:** team totals re-sum to the season's 2,419 bonus points (asserted).

## Three views, drilling down
1. **By team** — total bonus banked per club, plus each club's share of the league total.
2. **By position** — each club's haul split GK/DEF/MID/FWD (100% stacked bar), with a
   within-team share table and the league-wide position split.
3. **By player** — top-20 bonus earners coloured by position, plus each club's single biggest
   contributor and how concentrated that club's bonus is on one asset.

## Headline reads
- **Arsenal (189)** top the league, with **Man Utd (185)** and **Man City (175)** behind;
  **Wolves (47)** and **Burnley (56)** trail — weak attacking output shows up directly.
- **Midfield is the bonus engine** league-wide (~45%), then DEF (~28%), FWD (~20%), GK ~7%.
- **Position mix is a fingerprint:** Man Utd MID-led (103/185), Man City FWD-tilted (Haaland),
  while **Crystal Palace** is the outlier — DEF (52) outscores MID (23).
- **Individual magnets:** Haaland (43) and Bruno Fernandes (41) tower over the field.

## Caveats
- Team label is the player's per-GW `team`; a mid-season transfer splits a player's bonus
  across both clubs (correct for club attribution, but the player appears twice by name).
- Bonus is the raw awarded value — a retrospective of what happened, not a BPS prediction.
- Single completed season; no fixture or repeatability read here.
