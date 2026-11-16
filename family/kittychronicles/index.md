---
layout: page
title: The Kitty Chronicles
permalink: /family/kittychronicles/
---

Bedtime Bible stories starring Uncle Jonathan, his three fearless nieces and nephews, and (of course) the kittens who keep sneaking into the plot.

<p style="font-size:0.9em;color:#666;"><a href="{{ '/family/' | relative_url }}">&larr; Back to Family</a></p>

---

## Volume 2

<article style="display:flex;gap:1.25em;align-items:flex-start;margin-bottom:2em;padding:1.25em;border:1px solid #ddd;border-radius:8px;background:#fafafa;">
  <a href="{{ '/family/kittychronicles/volume-2/' | relative_url }}" style="flex-shrink:0;"><img src="{{ '/assets/images/family/kittychronicles/volume-2/peter-at-the-door.png' | relative_url }}" alt="Kitty Chronicles Volume 2" style="width:180px;height:120px;object-fit:cover;border-radius:6px;"></a>
  <div>
    <h3 style="margin:0 0 0.35em;"><a href="{{ '/family/kittychronicles/volume-2/' | relative_url }}">Kitty Chronicles Volume 2</a></h3>
    <p style="margin:0 0 0.65em;color:#444;">Four new illustrated Bible adventures, released weekly on Mondays.</p>
    <p style="margin:0;"><a href="{{ '/family/kittychronicles/volume-2/' | relative_url }}">Explore Volume 2 &rarr;</a></p>
  </div>
</article>

## Volume 1

{% assign stories = site.kittychronicles | sort: "order" %}

{% for story in stories %}
{% unless story.volume == 2 %}
<article style="display:flex;gap:1.25em;align-items:flex-start;margin-bottom:2em;">
  {% if story.image %}<a href="{{ story.url | relative_url }}" style="flex-shrink:0;"><img src="{{ story.image }}" alt="{{ story.title }}" style="width:140px;height:94px;object-fit:cover;border-radius:4px;"></a>{% endif %}
  <div>
    <h3 style="margin:0 0 0.25em;"><a href="{{ story.url | relative_url }}">{{ story.title }}</a></h3>
    {% if story.excerpt %}<p style="margin:0;font-size:0.95em;color:#444;">{{ story.excerpt }}</p>{% endif %}
  </div>
</article>
{% endunless %}
{% endfor %}
