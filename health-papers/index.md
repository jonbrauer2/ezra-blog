---
layout: page
title: Health Papers
permalink: /health-papers/
---

Comprehensive health guides and resources with scientific references.

---

### Available Papers

{% assign papers = site.pages | where_exp: "p", "p.path contains 'health-papers/'" | where_exp: "p", "p.name != 'index.md'" | sort: "title" %}
{% for paper in papers %}
{{ forloop.index }}. [{{ paper.title }}]({{ paper.url | relative_url }}){% if paper.subtitle %} — *{{ paper.subtitle }}*{% endif %}
{% endfor %}

---

More papers coming soon.
