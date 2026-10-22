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
| **Family** | Shared discoveries suitable for browsing, learning, and exploring together. | 1 | [Open Family View](https://sheurich.github.io/curated/#scope=family) |
| **Kids & Youth** | Approachable, visual, and curiosity-sparking resources for younger explorers. | 1 | [Open Kids & Youth View](https://sheurich.github.io/curated/#scope=kids) |
| **Personal** | Deep reference, tools, essays, and specialized interests. | 1 | [Open Personal View](https://sheurich.github.io/curated/#scope=personal) |
| **Household** | Practical utilities, planning references, and everyday guides. | 0 | [Open Household View](https://sheurich.github.io/curated/#scope=household) |

## Resources by Category

### Arts & Culture

*Museums, visual art, music, history, and cultural archives.*

- **[The Last Museum](https://lastmuseum.com/)** (lastmuseum.com) — Search and browse over 6.3 million artworks across human history—from 3000 BC to the present—with timeline filtering and high-resolution museum plates.
  - *Scopes:* Family, Kids & Youth, Personal · *Tags:* `#art` `#museum` `#free`
  - *Note:* Great for exploring art history chronologically or searching by subject, artist, or era.

## Tag Index

- [`#art`](https://sheurich.github.io/curated/#tags=art) (1): [The Last Museum](https://lastmuseum.com/)
- [`#free`](https://sheurich.github.io/curated/#tags=free) (1): [The Last Museum](https://lastmuseum.com/)
- [`#museum`](https://sheurich.github.io/curated/#tags=museum) (1): [The Last Museum](https://lastmuseum.com/)

---

## Adding or Updating Resources

Resources live in [`data/resources.json`](data/resources.json) and follow [`schema/resources.schema.json`](schema/resources.schema.json).

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
