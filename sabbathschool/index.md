---
layout: page
title: Sabbath School
permalink: /sabbathschool/
---

Resources and discussion guides for adult Sabbath School leaders and participants.

---

{% assign guides = site.sabbathschool | where: "category", "lesson-guide" | sort: "date" | reverse %}
{% assign today_str = site.time | date: "%Y-%m-%d" %}

{% comment %} Find the current lesson — the most recent one whose date is in the past or today {% endcomment %}
{% assign current_lesson = nil %}
{% for post in guides %}
  {% assign post_date = post.date | date: "%Y-%m-%d" %}
  {% if post_date <= today_str and current_lesson == nil %}
    {% assign current_lesson = post %}
  {% endif %}
{% endfor %}

{% if current_lesson %}
<div style="background: #f0f4f0; border-left: 4px solid #4a7c59; padding: 1em 1.25em; margin-bottom: 2em; border-radius: 0 4px 4px 0;">
  <p style="margin: 0 0 0.25em; font-size: 0.8em; text-transform: uppercase; letter-spacing: 0.05em; color: #4a7c59; font-weight: bold;">Current Lesson</p>
  <h3 style="margin: 0 0 0.2em;"><a href="{{ current_lesson.url | relative_url }}">{{ current_lesson.title }}</a></h3>
  {% if current_lesson.lesson_dates %}<p style="margin: 0 0 0.4em; font-size: 0.9em; color: #555;">{{ current_lesson.lesson_dates }}{% if current_lesson.series %} &mdash; <em>{{ current_lesson.series }}</em>{% endif %}</p>{% endif %}
  {% if current_lesson.excerpt %}<p style="margin: 0; font-size: 0.95em;">{{ current_lesson.excerpt }}</p>{% endif %}
</div>
{% endif %}

{% comment %} Group all guides by quarter {% endcomment %}
{% assign all_quarters = guides | map: "quarter" | uniq %}

{% for quarter in all_quarters %}
## {{ quarter }}

{% assign quarter_guides = guides | where: "quarter", quarter %}
{% assign series_name = quarter_guides.first.series %}
{% if series_name %}<p style="color: #555; margin-top: -0.75em; margin-bottom: 1em;"><em>{{ series_name }}</em></p>{% endif %}

{% for post in quarter_guides %}
  <article style="margin-bottom: 1.25em;">
    <h4 style="margin-bottom: 0.15em;"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h4>
    {% if post.lesson_dates %}<p style="margin: 0; font-size: 0.85em; color: #666;">{{ post.lesson_dates }}</p>{% endif %}
    {% if post.excerpt %}<p style="margin-top: 0.3em; font-size: 0.95em;">{{ post.excerpt }}</p>{% endif %}
  </article>
{% endfor %}

---
{% endfor %}

## Reference & Background

{% assign refs = site.sabbathschool | where_exp: "post", "post.category != 'lesson-guide'" | sort: "date" | reverse %}
{% for post in refs %}
  <article style="margin-bottom: 1.5em;">
    <h3 style="margin-bottom: 0.2em;"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    {% if post.excerpt %}<p style="margin-top: 0.4em;">{{ post.excerpt }}</p>{% endif %}
  </article>
{% endfor %}
