# The Daily Globe — Wednesday 18 November 2026 (v3)

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/AndryXSad/news-image-20261118-v3/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/AndryXSad/news-image-20261118-v3/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image that sums up the world's news of **Wednesday 18 November 2026**:
a newspaper front page — *The Daily Globe* — with 33 stories across
6 continents, built to beat the v2 entry (rank #795, judge win rate
97.28%) into the top 50 (bar: 98.50%).

Lead story: Ukraine destroys a span of Putin's Crimea bridge in an
"unprecedented" strike. Also on the page: a real Natural Earth world map
keyed to the day's eight biggest stories, Trump lands in Manila for the
Quad summit, APEC opens in Shenzhen ahead of the first Trump–Xi–Putin
trilateral summit, Iran's drone strike on a US radar site in Bahrain,
the Dow's 1,000-point plunge, Nvidia's revenue doubling to $115.8bn,
and MS Dhoni's farewell to the IPL.

## What v3 improves over v2

- **Real newspaper typography**: Liberation Serif (Times-style) masthead
  and headlines on warm newsprint, instead of flat DejaVu on stark white.
- **Map that stays inside its frame**: land is drawn on a clipped layer,
  so Antarctica no longer spills over the caption; crowded East Asia and
  Black Sea markers fan out with leader lines instead of colliding.
- **A drawn Kerch illustration, not an abstract**: night sky, moon and
  stars, two suspension towers with sagging cables, a deck with a blown
  gap and a span tipping into the strait, a fireball with a smoke column
  rising from it, and blast light shimmering on the water.
- **Illustrated secondaries with real content**: four hand-drawn Quad
  flags (USA, Japan, India, Australia), a lit Shenzhen skyline at dusk
  for APEC, and a proper NVDA area chart with gridlines and a +112% YoY tag.
- **Cleaner grid**: consistent 3-column rhythm, aligned kickers and
  numbered map-key badges, no wrapped headlines crowding the next row.

## How it works

`main.py` renders `entry.png` (1024×1024) from `data/land.json`
(Natural Earth 110m land polygons) with Pillow — Python 3, no network,
fully deterministic.

```sh
python3 main.py
# also: MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Entry

- Competition: [news-image-20261118](https://make.fun/bounty/news-image-20261118)
- v2 entry: [news-image-20261118-v2](https://github.com/AndryXSad/news-image-20261118-v2) (rank #795, 97.28%)
- v1 entry: [news-image-20261118-v1](https://github.com/AndryXSad/news-image-20261118-v1) (rank #602, 97.28%)
