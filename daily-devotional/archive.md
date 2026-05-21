---
layout: page
title: Devotional Archive
permalink: /daily-devotional/archive/
---

All devotionals, grouped by week, newest first.

---

{% assign all_devos = site.devotionals | sort: 'date' | reverse %}

{% assign seen_weeks = "" %}
{% for devo in all_devos %}
  {% if devo.week_start %}
    {% assign wk = devo.week_start %}
    {% unless seen_weeks contains wk %}
      {% assign seen_weeks = seen_weeks | append: wk | append: "|" %}
      {% assign week_devos = site.devotionals | where: "week_start", wk | sort: "date" %}
      {% assign week_label = week_devos.first.week_dates | default: wk %}

## Week of {{ week_label }}

      {% for wd in week_devos %}
* **{{ wd.date | date: "%A, %B %-d" }}** &mdash; [{{ wd.title }}]({{ wd.url | relative_url }}){% if wd.scripture %} *({{ wd.scripture }})*{% endif %}
      {% endfor %}

    {% endunless %}
  {% endif %}
{% endfor %}

{% assign legacy = site.devotionals | where_exp: "d", "d.week_start == nil" | sort: "date" | reverse %}
{% if legacy.size > 0 %}

## Earlier devotionals

{% for wd in legacy %}
* {{ wd.date | date: "%B %-d, %Y" }} &mdash; [{{ wd.title }}]({{ wd.url | relative_url }})
{% endfor %}

{% endif %}
