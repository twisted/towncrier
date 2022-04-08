{% if top_line %}
{{ top_line }}
{{ top_underline * ((top_line)|length)}}
{% elif versiondata.name %}
{{ versiondata.name }} {{ versiondata.version }} ({{ versiondata.date }} / {{ versiondata.date|date:"D d M Y" }})
{{ top_underline * ((versiondata.name + versiondata.version)|length + 4)}}{{ top_underline * (versiondata.date|title|length)}}
{% else %}
{{ versiondata.version }} ({{ versiondata.date }} # {{ versiondata.date|date:"D d M Y" }})
{{ top_underline * (versiondata.version|length + 3)}}{{ top_underline * (versiondata.date|title|length)}}
{% endif %}
{% for section, _ in sections.items() %}
{% set underline = underlines[0] %}{% if section %}{{section}}
{{ underline * section|length }}{% set underline = underlines[1] %}

{% endif %}

{% if sections[section] %}
{% for category, val in definitions.items() if category in sections[section]%}
{{ definitions[category]['name'] }}
{{ underline * definitions[category]['name']|length }}

{% if definitions[category]['showcontent'] %}
{% for text, values in sections[section][category].items() %}
- {{ text }} ({{ values|join(', ') }})
{% endfor %}

{% else %}
- {{ sections[section][category]['']|join(', ') }}

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


