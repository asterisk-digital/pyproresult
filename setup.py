#!/usr/bin/env python

from codecs import open

from setuptools import setup

requires = []
test_requirements = []

with open("README.md", "r", "utf-8") as f:
    readme = f.read()

github_link = "https://github.com/intrix-as/pyproresult"

setup(
    name="pyproresult",
    version="0.0.1",
    description="Library for interfacing with ProResult API",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="David Skoland",
    author_email="davidskoland@gmail.com",
    url=github_link,
    packages=["pyproresult"],
    package_data={"": ["LICENSE"]},
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=requires,
    license="MIT",
    zip_safe=False,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    tests_require=test_requirements,
    project_urls={
        "Documentation": github_link,
        "Source": github_link,
    },
)
