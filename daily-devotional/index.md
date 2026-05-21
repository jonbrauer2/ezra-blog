---
layout: page
title: Daily Devotional
permalink: /daily-devotional/
---

Morning devotionals posted daily, aligned with the current Sabbath School lesson themes.

---

{% assign all_devos = site.devotionals | sort: 'date' | reverse %}

{% comment %}Find today's devotional (most recent where date <= now){% endcomment %}
{% assign current_found = false %}
{% for devo in all_devos %}
  {% unless current_found %}
    {% assign devo_ts = devo.date | date: "%s" | plus: 0 %}
    {% assign now_ts = site.time | date: "%s" | plus: 0 %}
    {% if devo_ts <= now_ts %}
      {% assign current_devo = devo %}
      {% assign current_found = true %}
    {% endif %}
  {% endunless %}
{% endfor %}

{% if current_found %}
<div style="background:#f0f4f0;border-left:4px solid #4a7c59;padding:1em 1.25em;margin-bottom:2em;border-radius:0 4px 4px 0;">
  <p style="margin:0 0 0.25em;font-size:0.8em;text-transform:uppercase;letter-spacing:0.05em;color:#4a7c59;font-weight:bold;">Today's Devotional</p>
  <div style="display:flex;gap:1em;align-items:flex-start;">
    {% if current_devo.image %}<a href="{{ current_devo.url | relative_url }}" style="flex-shrink:0;"><img src="{{ current_devo.image }}" alt="{{ current_devo.title }}" style="width:120px;height:80px;object-fit:cover;border-radius:4px;"></a>{% endif %}
    <div>
      <h3 style="margin:0 0 0.2em;"><a href="{{ current_devo.url | relative_url }}">{{ current_devo.title }}</a></h3>
      <p style="margin:0 0 0.3em;font-size:0.9em;color:#555;">{{ current_devo.date | date: "%A, %B %-d, %Y" }}{% if current_devo.scripture %} &mdash; <em>{{ current_devo.scripture }}</em>{% endif %}</p>
      {% if current_devo.excerpt %}<p style="margin:0;font-size:0.95em;">{{ current_devo.excerpt }}</p>{% endif %}
    </div>
  </div>
</div>
{% endif %}

---

{% comment %}Group devotionals by week_start, newest week first{% endcomment %}
{% assign seen_weeks = "" %}
{% assign devos_with_week = "" %}
{% for devo in all_devos %}
  {% if devo.week_start %}
    {% assign wk = devo.week_start %}
    {% unless seen_weeks contains wk %}
      {% assign seen_weeks = seen_weeks | append: wk | append: "|" %}
      {% assign week_devos = site.devotionals | where: "week_start", wk | sort: "date" %}
      {% assign is_current_week = false %}
      {% if current_devo.week_start == wk %}{% assign is_current_week = true %}{% endif %}
      {% assign week_label = week_devos.first.week_dates | default: wk %}

      {% if is_current_week %}

## Week of {{ week_label }}

      {% for wd in week_devos %}
<article style="display:flex;gap:1em;align-items:flex-start;margin-bottom:1.5em;{% if wd.url == current_devo.url %}padding-left:0.75em;border-left:3px solid #4a7c59;{% endif %}">
  {% if wd.image %}<a href="{{ wd.url | relative_url }}" style="flex-shrink:0;"><img src="{{ wd.image }}" alt="{{ wd.title }}" style="width:100px;height:67px;object-fit:cover;border-radius:3px;"></a>{% endif %}
  <div>
    <p style="margin:0;font-size:0.75em;text-transform:uppercase;letter-spacing:0.05em;color:#888;">{{ wd.date | date: "%A, %B %-d" }}</p>
    <h4 style="margin:0.1em 0 0.1em;"><a href="{{ wd.url | relative_url }}">{{ wd.title }}</a></h4>
    {% if wd.scripture %}<p style="margin:0;font-size:0.85em;color:#666;"><em>{{ wd.scripture }}</em></p>{% endif %}
    {% if wd.excerpt %}<p style="margin-top:0.3em;font-size:0.9em;">{{ wd.excerpt }}</p>{% endif %}
  </div>
</article>
      {% endfor %}

      {% else %}

<details style="margin-bottom:1em;">
<summary style="cursor:pointer;font-size:1.1em;font-weight:bold;padding:0.4em 0;">Week of {{ week_label }} <span style="font-size:0.8em;font-weight:normal;color:#888;">({{ week_devos.size }} devotionals)</span></summary>
<div style="padding:0.5em 0 0 0.5em;">
      {% for wd in week_devos %}
<article style="display:flex;gap:1em;align-items:flex-start;margin-bottom:1.25em;">
  {% if wd.image %}<a href="{{ wd.url | relative_url }}" style="flex-shrink:0;"><img src="{{ wd.image }}" alt="{{ wd.title }}" style="width:80px;height:54px;object-fit:cover;border-radius:3px;opacity:0.85;"></a>{% endif %}
  <div>
    <p style="margin:0;font-size:0.75em;text-transform:uppercase;letter-spacing:0.05em;color:#888;">{{ wd.date | date: "%A, %B %-d" }}</p>
    <h4 style="margin:0.1em 0 0.1em;"><a href="{{ wd.url | relative_url }}">{{ wd.title }}</a></h4>
    {% if wd.scripture %}<p style="margin:0;font-size:0.85em;color:#666;"><em>{{ wd.scripture }}</em></p>{% endif %}
    {% if wd.excerpt %}<p style="margin-top:0.25em;font-size:0.88em;color:#444;">{{ wd.excerpt }}</p>{% endif %}
  </div>
</article>
      {% endfor %}
</div>
</details>

      {% endif %}
    {% endunless %}
  {% endif %}
{% endfor %}

{% comment %}Earlier devotionals — files without week_start{% endcomment %}
{% assign legacy = site.devotionals | where_exp: "d", "d.week_start == nil" | sort: "date" | reverse %}
{% if legacy.size > 0 %}

<details style="margin-bottom:1em;">
<summary style="cursor:pointer;font-size:1.1em;font-weight:bold;padding:0.4em 0;">Earlier devotionals <span style="font-size:0.8em;font-weight:normal;color:#888;">({{ legacy.size }} entries)</span></summary>
<div style="padding:0.5em 0 0 0.5em;">
{% for wd in legacy %}
<article style="display:flex;gap:1em;align-items:flex-start;margin-bottom:1.25em;">
  {% if wd.image %}<a href="{{ wd.url | relative_url }}" style="flex-shrink:0;"><img src="{{ wd.image }}" alt="{{ wd.title }}" style="width:80px;height:54px;object-fit:cover;border-radius:3px;opacity:0.85;"></a>{% endif %}
  <div>
    <p style="margin:0;font-size:0.75em;text-transform:uppercase;letter-spacing:0.05em;color:#888;">{{ wd.date | date: "%A, %B %-d" }}</p>
    <h4 style="margin:0.1em 0 0.1em;"><a href="{{ wd.url | relative_url }}">{{ wd.title }}</a></h4>
    {% if wd.scripture %}<p style="margin:0;font-size:0.85em;color:#666;"><em>{{ wd.scripture }}</em></p>{% endif %}
  </div>
</article>
{% endfor %}
</div>
</details>

{% endif %}

---

Subscribe via [RSS]({{ "/feed.xml" | relative_url }}) to receive new devotionals automatically.
