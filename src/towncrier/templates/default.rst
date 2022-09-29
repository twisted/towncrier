{% if render_title %}
{% set version_title %}
{% if versiondata.name %}
{{ versiondata.name }} {{ versiondata.version }} ({{ versiondata.date }}){% else %}
{{ versiondata.version }} ({{ versiondata.date }}){% endif %}
{% endset %}
{{ title_prefix }}{{ version_title }}
{% if top_underline %}
{{ top_underline * (version_title|length) }}
{% endif %}
{% endif %}
{% for section, _ in sections.items() %}
{% set underline = underlines[0] %}
{% if section %}
{{ section_prefix }}{{ section }}
{% if underline %}
{{ underline * section|length }}
{% endif %}
{% set underline = underlines[1] %}
{% endif %}

{% if sections[section] %}
{% for category, val in definitions.items() if category in sections[section]%}
{{ category_prefix }}{{ definitions[category]['name'] }}
{% if underline %}
{{ underline * definitions[category]['name']|length }}
{% endif %}

{% if definitions[category]['showcontent'] %}
{% for text, values in sections[section][category].items() %}
{{ bullet }}{{ text }}{% if values %} ({{ values|join(', ') }}){% endif %}

{% if issues_spaced and not loop.last %}

{% endif %}
{% endfor %}

{% else %}
{{ bullet }}{{ sections[section][category]['']|join(', ') }}

{% endif %}
{% if not sections[section][category] %}
No significant changes.

{% else %}
{% endif %}

{% endfor %}
{% else %}
No significant changes.


{% endif %}
{% endfor %}
