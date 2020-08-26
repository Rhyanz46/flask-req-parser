sudo rm -r __pycache__
sudo rm -R build
sudo rm -R dist
sudo rm -R Flask_Req_Parser.egg-info 
python setup.py sdist bdist_wheel
# pipenv install -e .
# env install -e .
twine upload --repository testpypi dist/*