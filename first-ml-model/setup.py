import pathlib
from setuptools import setup, find_packages    # or find_namespace_packages
# below python 3.3
# from distutils.core import setup

VERSION = '0.9.0'

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")
# Get install requires from requirements file
install_requires = open((here / "requirements.txt")).readlines()

setup(
    name="sklearn-fastapi",
    version=VERSION,
    description="machine learning model serving tempalte project with fastapi",
    long_description=long_description,
    long_description_content_type="text/markdown",

    # Optional
    url="https://github.com/hdouhua/ml-in-action/tree/main/first-ml-model",
    author="douhua",
    author_email="hdouhua@gmail.com",

    # Optional
    classifiers=[
        "Development Status :: Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: ML Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=
    "machine learning, model serving, sklearn, fastapi, sample, development",

    # Required
    package_dir={"": "app"},    # Optional
    # packages=find_packages(
    #     where='app',    # '.' by default
    #     include=['*'],    # ['*'] by default
    #     # exclude=[],    # empty by default
    # ),
    # packages=['app'],

    #
    python_requires=">=3.6",
    install_requires= install_requires,
    # install_requires=[
    #     'scikit-learn',
    #     'fastapi',
    #     'uvicorn',
    # ],

    # # data
    package_data={'': ['*.gz']}
    # data_files=["app/models/ml/iris_dt_v1.gz"],
    # include_package_data=True,

    # # Optional
    # entry_points={
    #     "console_scripts": [],
    # },
)