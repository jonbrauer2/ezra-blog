---
layout: page
title: Sabbath School
permalink: /sabbathschool/
---

Resources and discussion guides for adult Sabbath School leaders and participants.

---

{% assign guides = site.sabbathschool | where: "category", "lesson-guide" | sort: "date" %}

{% comment %}Find the current lesson: most recent one that isn't in the future{% endcomment %}
{% assign current_lesson_found = false %}
{% assign guides_reversed = guides | reverse %}
{% for post in guides_reversed %}
  {% unless current_lesson_found %}
    {% assign post_ts = post.date | date: "%s" | plus: 0 %}
    {% assign now_ts = site.time | date: "%s" | plus: 0 %}
    {% if post_ts <= now_ts %}
      {% assign current_lesson = post %}
      {% assign current_quarter = post.quarter %}
      {% assign current_lesson_found = true %}
    {% endif %}
  {% endunless %}
{% endfor %}

{% if current_lesson_found %}
<div style="background:#f0f4f0;border-left:4px solid #4a7c59;padding:1em 1.25em;margin-bottom:2em;border-radius:0 4px 4px 0;">
  <p style="margin:0 0 0.25em;font-size:0.8em;text-transform:uppercase;letter-spacing:0.05em;color:#4a7c59;font-weight:bold;">Current Lesson</p>
  <h3 style="margin:0 0 0.2em;"><a href="{{ current_lesson.url | relative_url }}">{{ current_lesson.title }}</a></h3>
  {% if current_lesson.lesson_dates %}<p style="margin:0 0 0.4em;font-size:0.9em;color:#555;">{{ current_lesson.lesson_dates }}{% if current_lesson.series %} &mdash; <em>{{ current_lesson.series }}</em>{% endif %}</p>{% endif %}
  {% if current_lesson.excerpt %}<p style="margin:0;font-size:0.95em;">{{ current_lesson.excerpt }}</p>{% endif %}
</div>
{% endif %}

---

{% comment %}Build ascending list of unique quarters{% endcomment %}
{% assign seen_quarters = "" %}
{% for post in guides %}
  {% assign q = post.quarter %}
  {% unless seen_quarters contains q %}
    {% assign seen_quarters = seen_quarters | append: q | append: "|" %}
    {% assign quarter_posts = guides | where: "quarter", q %}
    {% assign is_current = false %}
    {% if q == current_quarter %}{% assign is_current = true %}{% endif %}

    {% if is_current %}

## {{ q }}
{% if quarter_posts.first.series %}<p style="color:#555;margin-top:-0.5em;font-style:italic;">{{ quarter_posts.first.series }}</p>{% endif %}

    {% for qpost in quarter_posts %}
<article style="margin-bottom:1.1em;{% if qpost.url == current_lesson.url %}padding-left:0.75em;border-left:3px solid #4a7c59;{% endif %}">
  <h4 style="margin-bottom:0.1em;"><a href="{{ qpost.url | relative_url }}">{{ qpost.title }}</a></h4>
  {% if qpost.lesson_dates %}<p style="margin:0;font-size:0.85em;color:#666;">{{ qpost.lesson_dates }}</p>{% endif %}
</article>
    {% endfor %}

    {% else %}

<details style="margin-bottom:1em;">
<summary style="cursor:pointer;font-size:1.1em;font-weight:bold;padding:0.4em 0;">{{ q }}{% if quarter_posts.first.series %} &mdash; <span style="font-weight:normal;font-style:italic;">{{ quarter_posts.first.series }}</span>{% endif %} <span style="font-size:0.8em;font-weight:normal;color:#888;">({{ quarter_posts.size }} lessons)</span></summary>
<div style="padding:0.5em 0 0 0.5em;">
    {% for qpost in quarter_posts %}
<article style="margin-bottom:0.9em;">
  <h4 style="margin-bottom:0.1em;"><a href="{{ qpost.url | relative_url }}">{{ qpost.title }}</a></h4>
  {% if qpost.lesson_dates %}<p style="margin:0;font-size:0.85em;color:#666;">{{ qpost.lesson_dates }}</p>{% endif %}
</article>
    {% endfor %}
</div>
</details>

    {% endif %}
  {% endunless %}
{% endfor %}

---

## Reference & Background

{% assign refs = site.sabbathschool | where_exp: "post", "post.category != 'lesson-guide'" | sort: "date" | reverse %}
{% for post in refs %}
<article style="margin-bottom:1.5em;">
  <h3 style="margin-bottom:0.2em;"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
  {% if post.excerpt %}<p style="margin-top:0.4em;">{{ post.excerpt }}</p>{% endif %}
</article>
{% endfor %}
