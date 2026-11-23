---
layout: page
title: Kitty Chronicles Volume 2
permalink: /family/kittychronicles/volume-2/
---

Illustrated Bible adventures with Hadley, Grayson, Colton, Tumbles and Uncle Jonathan. New stories are proposed on Sundays and appear here only after review and approval.

<p style="font-size:0.9em;color:#666;"><a href="{{ '/family/' | relative_url }}">&larr; Back to Family</a></p>

---

{% assign stories = site.kittychronicles | where: "volume", 2 | sort: "order" %}

{% for story in stories %}
<article style="display:flex;gap:1.25em;align-items:flex-start;margin-bottom:2em;">
  {% if story.image %}<a href="{{ story.url | relative_url }}" style="flex-shrink:0;"><img src="{{ story.image }}" alt="{{ story.title }}" style="width:180px;height:120px;object-fit:cover;border-radius:6px;"></a>{% endif %}
  <div>
    <p style="margin:0 0 0.15em;font-size:0.8em;color:#777;text-transform:uppercase;letter-spacing:0.04em;">Story {{ story.order }} &middot; {{ story.date | date: "%B %-d, %Y" }}</p>
    <h3 style="margin:0 0 0.3em;"><a href="{{ story.url | relative_url }}">{{ story.title }}</a></h3>
    {% if story.excerpt %}<p style="margin:0;font-size:0.95em;color:#444;">{{ story.excerpt }}</p>{% endif %}
  </div>
</article>
{% endfor %}

<p style="margin-top:1em;color:#555;"><em>More adventures are added after each weekly proposal has been reviewed and merged.</em></p>
