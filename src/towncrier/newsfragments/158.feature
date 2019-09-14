There is now the option for ``all_bullets = false`` in the configuration.
Setting ``all_bullets`` to false means that news fragments have to include
the bullet point if they should be rendered as enumerations, otherwise
they are rendered directly (this means fragments can include a header.).
It is necessary to set this option to avoid (incorrect) automatic indentation
of multiline fragments that do not include bullet points.
The ``single-file-no-bullets.rst`` template gives an example of
using these options.
