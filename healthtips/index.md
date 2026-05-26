---
layout: page
title: Health Tips
permalink: /healthtips/
---

Evidence-based health insights from a biblical perspective. Natural remedies, nutritional guidance, and wellness wisdom for whole-person health.

---

{% assign all_tips = site.healthtips | sort: 'date' | reverse %}

{% comment %}Find the most recent tip whose date <= now{% endcomment %}
{% assign current_found = false %}
{% for tip in all_tips %}
  {% unless current_found %}
    {% assign tip_ts = tip.date | date: "%s" | plus: 0 %}
    {% assign now_ts = site.time | date: "%s" | plus: 0 %}
    {% if tip_ts <= now_ts %}
      {% assign current_tip = tip %}
      {% assign current_found = true %}
    {% endif %}
  {% endunless %}
{% endfor %}

{% if current_found %}
<div style="background:#f0f4f0;border-left:4px solid #4a7c59;padding:1em 1.25em;margin-bottom:2em;border-radius:0 4px 4px 0;">
  <p style="margin:0 0 0.25em;font-size:0.8em;text-transform:uppercase;letter-spacing:0.05em;color:#4a7c59;font-weight:bold;">Latest Tip</p>
  <div style="display:flex;gap:1em;align-items:flex-start;">
    {% if current_tip.image %}<a href="{{ current_tip.url | relative_url }}" style="flex-shrink:0;"><img src="{{ current_tip.image }}" alt="{{ current_tip.title }}" style="width:120px;height:80px;object-fit:cover;border-radius:4px;"></a>{% endif %}
    <div>
      <h3 style="margin:0 0 0.2em;"><a href="{{ current_tip.url | relative_url }}">{{ current_tip.title }}</a></h3>
      <p style="margin:0 0 0.3em;font-size:0.9em;color:#555;">{{ current_tip.date | date: "%A, %B %-d, %Y" }}</p>
      {% if current_tip.excerpt %}<p style="margin:0;font-size:0.95em;">{{ current_tip.excerpt | strip_html | truncatewords: 40 }}</p>{% endif %}
    </div>
  </div>
</div>
{% endif %}

---

{% comment %}Older tips — everything except the current one, only if its date <= now{% endcomment %}
{% for tip in all_tips %}
  {% assign tip_ts = tip.date | date: "%s" | plus: 0 %}
  {% assign now_ts = site.time | date: "%s" | plus: 0 %}
  {% if tip_ts <= now_ts and tip.url != current_tip.url %}
<article style="display:flex;gap:1em;align-items:flex-start;margin-bottom:1.5em;">
  {% if tip.image %}<a href="{{ tip.url | relative_url }}" style="flex-shrink:0;"><img src="{{ tip.image }}" alt="{{ tip.title }}" style="width:100px;height:67px;object-fit:cover;border-radius:3px;"></a>{% endif %}
  <div>
    <p style="margin:0;font-size:0.75em;text-transform:uppercase;letter-spacing:0.05em;color:#888;">{{ tip.date | date: "%B %-d, %Y" }}</p>
    <h4 style="margin:0.1em 0 0.1em;"><a href="{{ tip.url | relative_url }}">{{ tip.title }}</a></h4>
    {% if tip.excerpt %}<p style="margin-top:0.3em;font-size:0.9em;color:#444;">{{ tip.excerpt | strip_html | truncatewords: 30 }}</p>{% endif %}
  </div>
</article>
  {% endif %}
{% endfor %}

---

*Disclaimer: Information provided is for educational purposes only and should not replace professional medical advice. Always consult with a qualified healthcare provider before starting any new health regimen.*
