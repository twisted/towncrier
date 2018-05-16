Made ``package`` optional.
When the version is passed on the command line,
and the ``title_format`` does not use the package name,
and it is not used for the path to the news fragments,
then no package name is needed, so we should not enforce it.
