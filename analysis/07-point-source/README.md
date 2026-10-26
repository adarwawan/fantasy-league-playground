# 07 — Point-Source Contribution (2025/26 retrospective)

Two players finish on the same total and are completely different assets. We decompose each
top player's season into **where the points came from** — goals, assists, bonus, clean sheets,
the new **defensive-contribution** category, appearances, and deductions. Spec:
[brainstorming/14](../../brainstorming/14-point-source-contribution.md).

- **Notebook:** [point_source_contribution.ipynb](point_source_contribution.ipynb) (2025/26).
- **Data:** vaastav `2025-26/gws/merged_gw.csv` only — raw per-GW counts, no fixtures/teams.
- **CS framing:** additive attribution — decompose one scalar (`total_points`) into
  mutually-exclusive buckets, then normalise each to a **share** (concepts E + D, plus the
  attribution beat in [00](../../brainstorming/00-algorithms-reference.md)).

## The honest twist — a decomposition you can audit
The data gives raw *counts* (`goals_scored`, `assists`, …), not per-source points. We rebuild
every bucket from the FPL 2025/26 rules **per player-GW** (thresholds and floors —
appearance tiers, `saves // 3`, `goals_conceded // 2`, the 60-min clean-sheet gate, the DC
threshold — don't survive season-summing), then reconcile against `total_points`:

> **0 / 29,757 rows** with a non-zero residual — every bucket reconstructed exactly. The split
> is lossless, so every share below is auditable, not approximate.

## Scoring model (position-aware)
Goals GK/DEF ×6, MID ×5, FWD ×4 · Assists ×3 · Clean sheet GK/DEF 4, MID 1, FWD 0 (60+ min
only) · **Defensive contribution** +2/GW at DEF ≥10 (CBI) or MID/FWD ≥12 (CBIT/CBIR) · GK
+1/3 saves, +5 pen save · Deductions: −1 per 2 conceded (GK/DEF), −2 pen miss, −1 yellow,
−3 red, −2 own goal · Bonus taken as-is. All tunable in the Config cell.

## Universe
Top-K per position by **total points**: `TOP_PER_POS = {GK: 4, DEF: 10, MID: 10, FWD: 6}` (30
players), same shape as [#05](../05-fixture-proof/). Top-K by points already filters to
regulars, so no extra minutes guard.

## Normalisation
- **Positive-share columns** divide each positive bucket by **gross positive points**, so they
  sum to ~100% and drive the stacked bar.
- **`%deductions`** is reported separately — it's a *drag* on the total, not a slice of it, so
  folding it into the stack would be dishonest.

## Output
- **Table:** player | pos | team | pts | %appear | %goals | %assists | %CS | %DC | %GKpts |
  %bonus | %deduct.
- **Money shot:** 100% stacked horizontal bars, grouped by position, ordered by total points —
  reads left-to-right as "what kind of scorer is this".
- **Heatmap:** the same `player × source` shares as a grid.
- **Explosive-vs-grinder scatter:** attacking share (goals+assists) vs floor share
  (appearance+DC+clean sheets), bubble = total points — the bridge to #05 fixture-proofing.

## Headline reads
- **Most goal-dependent:** Igor Thiago (46.3% goals) and Haaland (44.4% goals, plus a
  league-leading 17.7% from bonus) — boom-or-bust, matchup-sensitive hauls.
- **The playmaker signature:** Bruno Fernandes leans on **assists (29.5%)** more than goals
  (18.4%) — the top MID's points are creation-led, not finishing-led.
- **Defensive-contribution grinders** (the new-category story): Elliot Anderson banks
  **27.7%** of his points from DC, with Senesi (25.7% for a DEF), Garner (23.4%), Lacroix and
  Tarkowski (~22.6%) close behind — near-guaranteed floor points that barely existed last year.
- **Keepers are clean-sheet-or-bust:** David Raya draws **44.7%** from clean sheets and just
  5.3% from saves; Kelleher/Roefs sit ~24–26% CS but 20–23% saves — busier keepers on worse
  defences.
- **Same total, different player:** Semenyo (202, 40% goals) and Gibbs-White (188, 40% goals)
  are twin explosive MIDs, while Anderson (180) on a similar total is almost entirely a
  floor/DC grinder — three "elite midfielders" that repeat for completely different reasons.

## Caveats
- Deductions are shown as a share of gross positive, not netted into the stack (by design).
- Team label is the player's most-frequent GW team (handles mid-season transfers loosely).
- Shares describe *what already happened*; repeatability (how fixture-sensitive each slice is)
  is the #05 cross-read, not proven here.
- Pre-2025/26 seasons lack the defensive-contribution category — a sibling notebook would drop
  that bucket, mirroring #05's dual-season setup.
