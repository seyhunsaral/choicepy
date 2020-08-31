# Building and Releasing 
for maintainers

* Update version numbers:
  * On `setup.py` change `version='X.X.X'`

* Release on PyPi 
  * Create package gzips by `python setup.py sdist bdist_wheel`
  * Upload by `twine upload dist/*`

* Merge develop to master
  * `git checkout master`
  * `git merge develop --no-ff` 
  * `git tag "vX.X.X"`
  
