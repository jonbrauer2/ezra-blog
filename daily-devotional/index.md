---
layout: page
title: Daily Devotional
permalink: /daily-devotional/
---

![Daily Devotional](/ezra-blog/assets/images/devotionals/daily-devotional-header.jpg)
*Photo by Isabella Mendes on Pexels*

# Daily Devotional

Morning devotionals posted every day at 5:30 AM EST, aligned with the current Sabbath School lesson. Each devotional includes:

- Scripture meditation
- Thoughtful reflection
- Practical application challenge
- Discussion-worthy insights

## Recent Devotionals

{% assign devotionals = site.devotionals | sort: 'date' | reverse %}
{% for devotional in devotionals limit:10 %}
  * {{ devotional.date | date: "%B %-d, %Y" }} - [{{ devotional.title }}]({{ devotional.url | relative_url }})
{% endfor %}

[View All Devotionals →](/ezra-blog/daily-devotional/archive/)

---

Subscribe via [RSS](/ezra-blog/feed.xml) to receive new devotionals automatically.
