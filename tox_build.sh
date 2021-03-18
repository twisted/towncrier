# build the sdist

set -evx

check-manifest ${toxinidir}
python -m build --sdist --outdir ${toxinidir}/dist/ ${toxinidir}
tar -xvf ${toxinidir}/dist/*
cd *
# build the wheel from the sdist
python -m build --wheel --outdir ${toxinidir}/dist/ .
