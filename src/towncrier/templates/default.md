{% if render_title %}
{% if versiondata.name %}
# {{ versiondata.name }} {{ versiondata.version }} ({{ versiondata.date }})
{% else %}
{{ versiondata.version }} ({{ versiondata.date }})
{% endif %}
{% endif %}
{% for section, _ in sections.items() %}
{% if section %}

## {{section}}
{% endif %}

{% if sections[section] %}
{% for category, val in definitions.items() if category in sections[section] %}
### {{ definitions[category]['name'] }}

{% if definitions[category]['showcontent'] %}
{% for text, values in sections[section][category].items() %}
- {{ text }}
{%- if values %}
{% if "\n  - " in text or '\n  * ' in text %}


  (
{%- else %}
 (
{%- endif -%}
{%- for issue in values %}
{{ issue.split(": ", 1)[0] }}{% if not loop.last %}, {% endif %}
{%- endfor %}
)
{% else %}

{% endif %}
{% endfor %}

{% else %}
- {% for issue in sections[section][category][''] %}
{{ issue.split(": ", 1)[0] }}{% if not loop.last %}, {% endif %}
{% endfor %}


{% endif %}
{% if issues_by_category[section][category] and "]: " in issues_by_category[section][category][0] %}
{% for issue in issues_by_category[section][category] %}
{{ issue }}
{% endfor %}

{% endif %}
{% if sections[section][category]|length == 0 %}
No significant changes.

{% else %}
{% endif %}
{% endfor %}
{% else %}
No significant changes.

{% endif %}
{% endfor %}
