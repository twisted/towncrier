Make ``towncrier create`` use the fragment counter rather than failing
on existing fragment names.

For example, if there is an existing fragment named ``123.feature``,
then ``towncrier create 123.feature`` will now create a fragment
named ``123.feature.1``.
