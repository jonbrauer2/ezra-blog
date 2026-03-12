---
layout: page
title: Devotional Archive
permalink: /daily-devotional/archive/
---

# Devotional Archive

All devotionals, newest first:

{% assign devotionals = site.devotionals | sort: 'date' | reverse %}
{% for devotional in devotionals %}
  * {{ devotional.date | date: "%B %-d, %Y" }} - [{{ devotional.title }}]({{ devotional.url | relative_url }})
{% endfor %}
