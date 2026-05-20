---
layout: page
title: Sabbath School
permalink: /sabbathschool/
---

Resources and discussion guides for adult Sabbath School leaders and participants.

---

{% assign guides = site.sabbathschool | where: "category", "lesson-guide" | sort: "date" | reverse %}

{% comment %}Current lesson: most recent post whose date is not in the future{% endcomment %}
{% assign current_lesson_found = false %}
{% for post in guides %}
  {% unless current_lesson_found %}
    {% assign post_date = post.date | date: "%s" | plus: 0 %}
    {% assign now = site.time | date: "%s" | plus: 0 %}
    {% if post_date <= now %}
      {% assign current_lesson = post %}
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

{% comment %}Group by quarter using a seen-quarters approach{% endcomment %}
{% assign seen_quarters = "" %}
{% for post in guides %}
  {% assign q = post.quarter %}
  {% unless seen_quarters contains q %}
    {% assign seen_quarters = seen_quarters | append: q | append: "|" %}

<h2>{{ q }}</h2>
{% if post.series %}<p style="color:#555;margin-top:-0.5em;"><em>{{ post.series }}</em></p>{% endif %}

    {% assign quarter_posts = guides | where: "quarter", q %}
    {% for qpost in quarter_posts %}
<article style="margin-bottom:1.25em;">
  <h4 style="margin-bottom:0.15em;"><a href="{{ qpost.url | relative_url }}">{{ qpost.title }}</a></h4>
  {% if qpost.lesson_dates %}<p style="margin:0;font-size:0.85em;color:#666;">{{ qpost.lesson_dates }}</p>{% endif %}
  {% if qpost.excerpt %}<p style="margin-top:0.3em;font-size:0.95em;">{{ qpost.excerpt }}</p>{% endif %}
</article>
    {% endfor %}

---

  {% endunless %}
{% endfor %}

## Reference & Background

{% assign refs = site.sabbathschool | where_exp: "post", "post.category != 'lesson-guide'" | sort: "date" | reverse %}
{% for post in refs %}
<article style="margin-bottom:1.5em;">
  <h3 style="margin-bottom:0.2em;"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
  {% if post.excerpt %}<p style="margin-top:0.4em;">{{ post.excerpt }}</p>{% endif %}
</article>
{% endfor %}
