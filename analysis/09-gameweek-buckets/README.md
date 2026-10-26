# 09 — Per-Gameweek Point Buckets (last season, 2025/26)

A season total tells you *how much*, never *what shape*. Two 150-point midfielders can arrive
via steady mid-single-digit weeks or via a handful of hauls stitched between blanks. We bucket
**every player-GW** of last season into four tiers and count how each player's season splits
across them.

- **Notebooks:** [gameweek_buckets.ipynb](gameweek_buckets.ipynb) (2025/26, vaastav CSV) and
  [gameweek_buckets_26.ipynb](gameweek_buckets_26.ipynb) (2026/27 season-to-date, official FPL API:
  `bootstrap-static` + `event/{gw}/live`, incl. the in-progress GW as provisional).
- **Data:** vaastav `2025-26/gws/merged_gw.csv` only — one row per player per gameweek, raw
  `total_points`. No fixtures, no rebuild of the scoring model needed.

## Buckets
On per-GW `total_points` (inclusive, tunable in the Config cell):

| bucket | range | reading |
|---|---|---|
| **blank** | ≤ 2 | played and returned nothing |
| **pre-return** | 3–4 | on the pitch, appearance points only |
| **return** | 5–9 | a goal / assist / clean-sheet–shaped haul |
| **double digit** | ≥ 10 | a ceiling week |

By default only GWs with `minutes > 0` are counted, so a player's **blank** count means *played
and blanked*, not *benched*. Flip `COUNT_NONPLAYING` in Config to include non-playing rows.

## CS framing
Discretise a continuous scalar (`total_points`) into ordered, non-overlapping bins, then
count-aggregate per player — a **per-player histogram** rendered as a 100% stacked share bar.
The bins are contiguous and exhaustive (asserted), so the split is lossless.

## Universe
Top-K per position by **total season points**: `TOP_PER_POS = {GK: 6, DEF: 15, MID: 15,
FWD: 9}` (45 players), same shape as [#07](../07-point-source/).

## Output (2026/27 notebook)
- **Config:** `MIN_MINUTES` (default 45; cameos are not blanks), `LOOKBACK` (last N GWs),
  `EXCLUDE_PROVISIONAL`, `RANK_BY` (`total_points` | `ppg`), `MIN_GAMES`.
- **Position baseline:** bucket mix over *all* counted player-GWs of each position — the
  reference for every chart (the top-K universe is selected on outcome, so it is biased high).
- **Table:** counts per bucket, `ppg`, `%ret+` with a Wilson 95% interval, the position
  baseline, and whether the interval clears it. No per-bucket shares: at ~7 GWs they are
  multiples of 1/n.
- **Tile strip (money shot):** player x GW grid coloured by bucket with points printed in each
  tile; grey = under `MIN_MINUTES`, dashed outline = provisional GW. Shows streaks and recency.
- **GW x position grid:** share of players reaching a return each week — the league context.
- **Boom-or-bust scatter:** blank share vs double-digit share, jittered, per-position markers, bubble area ~ points, labels de-collided with adjustText,
  X = position baseline, dotted = field baseline, only standouts labelled.

The 2025/26 notebook (`gameweek_buckets.ipynb`) still uses the original stacked-bar / heatmap
layout.
