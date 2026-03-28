---
layout: page
title: Sabbath School
permalink: /sabbathschool/
---

Resources, references, and reflections for adult Sabbath School discussion leaders and participants.

## Resources

{% for post in site.sabbathschool %}
  <article>
    <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    <time>{{ post.date | date: site.date_format }}</time>
    {% if post.excerpt %}
      <p>{{ post.excerpt }}</p>
    {% endif %}
  </article>
{% endfor %}
