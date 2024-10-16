from distutils.core import setup

setup(
    name="jsontodpg",
    version="0.93",
    description="Build DearPyGui user interface with json/python dictionaies",
    author="init-helpful",
    author_email="init.helpful@gmail.com",
    url="https://github.com/init-helpful/JsonToDpg",
    py_modules=[
        "jsontodpg",
        "dpgkeywords",
        "tokenizer",
        "dpgextended",
        "controller",
        "store",
        "jtodpgutils",
        "asyncfunction"
    ],
    install_requires=["dearpygui", "polars"],
    package_dir={"": "src"},
)
