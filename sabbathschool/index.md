---
layout: page
title: Sabbath School
permalink: /sabbathschool/
---

Resources and discussion guides for adult Sabbath School leaders and participants.

---

## Lesson Guides

Weekly discussion notes with theological depth, exegetical insights, and questions designed for experienced Adventists who want to wrestle seriously with Scripture.

{% assign guides = site.sabbathschool | where: "category", "lesson-guide" | sort: "date" | reverse %}
{% for post in guides %}
  <article style="margin-bottom: 1.5em;">
    <h3 style="margin-bottom: 0.2em;"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    {% if post.lesson_dates %}<p style="margin: 0; font-size: 0.9em; color: #666;">{{ post.lesson_dates }}{% if post.series %} &mdash; <em>{{ post.series }}</em>{% endif %}</p>{% endif %}
    {% if post.excerpt %}<p style="margin-top: 0.4em;">{{ post.excerpt }}</p>{% endif %}
  </article>
{% endfor %}

---

## Reference & Background

{% assign refs = site.sabbathschool | where_exp: "post", "post.category != 'lesson-guide'" | sort: "date" | reverse %}
{% for post in refs %}
  <article style="margin-bottom: 1.5em;">
    <h3 style="margin-bottom: 0.2em;"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    {% if post.excerpt %}<p style="margin-top: 0.4em;">{{ post.excerpt }}</p>{% endif %}
  </article>
{% endfor %}
