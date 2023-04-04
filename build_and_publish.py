import os
os.system("python setup.py sdist")
os.system("twine upload dist/*")