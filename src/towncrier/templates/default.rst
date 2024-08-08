{% if render_title %}
{% if versiondata.name %}
{{ versiondata.name }} {{ versiondata.version }} ({{ versiondata.date }})
{{ top_underline * (get_underline_length(versiondata.name + versiondata.version + versiondata.date) + 4)}}
{% else %}
{{ versiondata.version }} ({{ versiondata.date }})
{{ top_underline * (get_underline_length(versiondata.version + versiondata.date) + 3)}}
{% endif %}
{% endif %}
{% for section, _ in sections.items() %}
{% set underline = underlines[0] %}{% if section %}{{section}}
{{ underline * get_underline_length(section) }}{% set underline = underlines[1] %}

{% endif %}

{% if sections[section] %}
{% for category, val in definitions.items() if category in sections[section]%}
{{ definitions[category]['name'] }}
{{ underline * get_underline_length(definitions[category]['name']) }}

{% for text, values in sections[section][category].items() %}
- {% if text %}{{ text }}{% if values %} ({{ values|join(', ') }}){% endif %}{% else %}{{ values|join(', ') }}{% endif  %}

{% endfor %}

{% if get_underline_length(sections[section][category]) == 0 %}
No significant changes.

{% else %}
{% endif %}

{% endfor %}
{% else %}
No significant changes.


{% endif %}
{% endfor %}
