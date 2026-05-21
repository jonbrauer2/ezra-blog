---
layout: page
title: Health Papers
permalink: /health-papers/
---

Comprehensive health guides and resources with scientific references.

---

### Available Papers

- [Hydrotherapy for Common Cold Relief: An Evidence-Based Guide](hydrotherapy-for-common-cold-relief.html)
- [Evidence-Based Guide to Alzheimer's Disease Prevention and Cognitive Health: Lifestyle Medicine Strategies for Brain Health](/ezra-blog/health-papers/alzheimers-prevention-guide/)

---

More papers coming soon.

{% comment %}
Auto-listing alternative — switch to this when you've migrated all papers to .md
with front-matter titles. Drops the hand-maintained list above.

  {% assign papers = site.html_pages | where_exp: "p", "p.path contains 'health-papers/'" | where_exp: "p", "p.name != 'index.md'" | sort: "title" %}
  {% for paper in papers %}
  - [{{ paper.title }}]({{ paper.url | relative_url }}){% if paper.subtitle %} — *{{ paper.subtitle }}*{% endif %}
  {% endfor %}
{% endcomment %}
