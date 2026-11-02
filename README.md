# Curated

> A minimalist index of enduring internet resources for personal and family exploration.

**Live Site:** [https://sheurich.github.io/curated/](https://sheurich.github.io/curated/)

A curated directory of enduring internet resources for personal and family use, organized across multiple views and scopes:

- **Cards View:** [`#view=cards`](https://sheurich.github.io/curated/#view=cards) — Editorial cards with descriptions, notes, scopes, and tags
- **Compact Index:** [`#view=index`](https://sheurich.github.io/curated/#view=index) — Dense table view for rapid scanning
- **Category Directory:** [`#view=directory`](https://sheurich.github.io/curated/#view=directory) — Grouped by subject area
- **Tag Atlas:** [`#view=tags`](https://sheurich.github.io/curated/#view=tags) — Cross-referenced tag matrix

---

## Browse by Scope

| Scope | Description | Entries | Direct View |
| :--- | :--- | :---: | :--- |
| **Family** | Shared discoveries suitable for browsing, learning, and exploring together. | 4 | [Open Family View](https://sheurich.github.io/curated/#scope=family) |
| **Kids & Youth** | Approachable, visual, and curiosity-sparking resources for younger explorers. | 3 | [Open Kids & Youth View](https://sheurich.github.io/curated/#scope=kids) |
| **Personal** | Deep reference, tools, essays, and specialized interests. | 4 | [Open Personal View](https://sheurich.github.io/curated/#scope=personal) |
| **Household** | Practical utilities, planning references, and everyday guides. | 0 | [Open Household View](https://sheurich.github.io/curated/#scope=household) |

## Resources by Category

### Arts & Culture

*Museums, visual art, music, history, and cultural archives.*

- **[The Last Museum](https://lastmuseum.com/)** (lastmuseum.com) — Search and browse over 6.3 million artworks across human history—from 3000 BC to the present—with timeline filtering and high-resolution museum plates.
  - *Scopes:* Family, Kids & Youth, Personal · *Tags:* `#art` `#museum` `#free`
  - *Note:* Great for exploring art history chronologically or searching by subject, artist, or era.

### Learning & Reference

*Encyclopedias, explainers, interactive courses, and deep dives.*

- **[F/OSS Comics](https://fosscomics.com/)** (fosscomics.com) — Illustrated comic series exploring the history of computing, Unix, and free and open-source software—from Bell Labs and Dennis Ritchie to BSD Unix and the birth of the vi editor.
  - *Scopes:* Family, Kids & Youth, Personal · *Tags:* `#comics` `#computing-history` `#open-source` `#unix` `#free`
  - *Note:* Approachable visual storytelling that makes operating-system history, the Unix philosophy, and classic software engineering accessible for both older kids and adults.

### Reading & Media

*Books, public domain libraries, audio, and thoughtful publications.*

- **[Hacker Books](https://hackerbooks.org/)** (hackerbooks.org) — Search and browse over 16,000 books mentioned across Hacker News comment threads since 2007, ranked by distinct recommendations, rising trends, and 29 subject categories.
  - *Scopes:* Personal, Family · *Tags:* `#books` `#reading` `#recommendations` `#programming` `#free`
  - *Note:* Links every book directly to the original Hacker News comment threads where readers discussed or recommended it—great for finding deeply vetted computing, science, history, and sci-fi reads.

### Making & Play

*Puzzles, crafts, games, and hands-on projects.*

- **[Neal.fun](https://neal.fun/)** (neal.fun) — Interactive micro-games, playful simulations, and visual web experiments by Neal Agarwal—from Infinite Craft and The Password Game to exploring the deep sea and outer space.
  - *Scopes:* Family, Kids & Youth, Personal · *Tags:* `#games` `#interactive` `#play` `#science` `#free`
  - *Note:* Great for kids and family browsing; standout experiments include Infinite Craft, The Deep Sea, The Size of Space, Internet Artifacts, and The Password Game.

## Tag Index

- [`#art`](https://sheurich.github.io/curated/#tags=art) (1): [The Last Museum](https://lastmuseum.com/)
- [`#books`](https://sheurich.github.io/curated/#tags=books) (1): [Hacker Books](https://hackerbooks.org/)
- [`#comics`](https://sheurich.github.io/curated/#tags=comics) (1): [F/OSS Comics](https://fosscomics.com/)
- [`#computing-history`](https://sheurich.github.io/curated/#tags=computing-history) (1): [F/OSS Comics](https://fosscomics.com/)
- [`#free`](https://sheurich.github.io/curated/#tags=free) (4): [The Last Museum](https://lastmuseum.com/), [Neal.fun](https://neal.fun/), [Hacker Books](https://hackerbooks.org/), [F/OSS Comics](https://fosscomics.com/)
- [`#games`](https://sheurich.github.io/curated/#tags=games) (1): [Neal.fun](https://neal.fun/)
- [`#interactive`](https://sheurich.github.io/curated/#tags=interactive) (1): [Neal.fun](https://neal.fun/)
- [`#museum`](https://sheurich.github.io/curated/#tags=museum) (1): [The Last Museum](https://lastmuseum.com/)
- [`#open-source`](https://sheurich.github.io/curated/#tags=open-source) (1): [F/OSS Comics](https://fosscomics.com/)
- [`#play`](https://sheurich.github.io/curated/#tags=play) (1): [Neal.fun](https://neal.fun/)
- [`#programming`](https://sheurich.github.io/curated/#tags=programming) (1): [Hacker Books](https://hackerbooks.org/)
- [`#reading`](https://sheurich.github.io/curated/#tags=reading) (1): [Hacker Books](https://hackerbooks.org/)
- [`#recommendations`](https://sheurich.github.io/curated/#tags=recommendations) (1): [Hacker Books](https://hackerbooks.org/)
- [`#science`](https://sheurich.github.io/curated/#tags=science) (1): [Neal.fun](https://neal.fun/)
- [`#unix`](https://sheurich.github.io/curated/#tags=unix) (1): [F/OSS Comics](https://fosscomics.com/)

---

## Adding or Updating Resources

Resources live in [`data/resources.json`](data/resources.json) and follow [`schema/resources.schema.json`](schema/resources.schema.json).

### In Pi (`/add` skill & command)

```text
/add neal.fun games site
```

### Quick CLI (`scripts/curate.py`)

```bash
# Add a resource and rebuild the site + README
python3 scripts/curate.py add \
  --url "https://lastmuseum.com/" \
  --title "The Last Museum" \
  --tags "art,museum,free" \
  --category "arts-culture" \
  --scopes "family,kids,personal" \
  --description "Search and browse over 6.3 million artworks across human history."

# Validate data and regenerate site/ + README.md
python3 scripts/build.py
```
