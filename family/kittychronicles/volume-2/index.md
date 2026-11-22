---
layout: page
title: Kitty Chronicles Volume 2
permalink: /family/kittychronicles/volume-2/
---

Four new illustrated Bible adventures with Uncle Jonathan, Hadley, Grayson, Colton and a kitten who always seems to arrive just in time. A new story is released every Monday.

<p style="font-size:0.9em;color:#666;"><a href="{{ '/family/' | relative_url }}">&larr; Back to Family</a></p>

---

{% assign stories = site.kittychronicles | where: "volume", 2 | sort: "order" %}
{% assign now_seconds = site.time | date: "%s" | plus: 0 %}
{% assign next_story = nil %}

{% for story in stories %}
  {% assign story_seconds = story.date | date: "%s" | plus: 0 %}
  {% if story_seconds <= now_seconds %}
<article style="display:flex;gap:1.25em;align-items:flex-start;margin-bottom:2em;">
  {% if story.image %}<a href="{{ story.url | relative_url }}" style="flex-shrink:0;"><img src="{{ story.image }}" alt="{{ story.title }}" style="width:180px;height:120px;object-fit:cover;border-radius:6px;"></a>{% endif %}
  <div>
    <p style="margin:0 0 0.15em;font-size:0.8em;color:#777;text-transform:uppercase;letter-spacing:0.04em;">Story {{ story.order }} &middot; {{ story.date | date: "%B %-d, %Y" }}</p>
    <h3 style="margin:0 0 0.3em;"><a href="{{ story.url | relative_url }}">{{ story.title }}</a></h3>
    {% if story.excerpt %}<p style="margin:0;font-size:0.95em;color:#444;">{{ story.excerpt }}</p>{% endif %}
  </div>
</article>
  {% elsif next_story == nil %}
    {% assign next_story = story %}
  {% endif %}
{% endfor %}

{% if next_story %}
<aside style="margin-top:1em;padding:1em 1.15em;border-left:4px solid #6f8f3d;background:#f6f8f1;">
  <strong>Next adventure:</strong> {{ next_story.title }} arrives {{ next_story.date | date: "%A, %B %-d" }}.
</aside>
{% else %}
<p style="margin-top:1em;color:#555;"><em>All four Volume 2 adventures are now available.</em></p>
{% endif %}
