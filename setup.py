from distutils.core import setup

setup(
    name="jsontodpg",
    version="1.3",
    description="Build DearPyGui user interface with json/python dictionaies",
    author="init-helpful",
    author_email="init.helpful@gmail.com",
    url="https://github.com/init-helpful/JsonToDpg",
    py_modules=["jsontodpg","dpgkeywords",'tokenizer'],
    install_requires=["dearpygui"],
    package_dir={"": "src"},
)
