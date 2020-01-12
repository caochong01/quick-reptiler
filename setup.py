# -*- coding: utf-8 -*-
import io

from setuptools import find_packages
from setuptools import setup

# TODO 项目的部署文件

with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="bhcrjy",
    version="1.0.0",
    url="",
    license="BSD",
    maintainer="Pallets team",
    maintainer_email="caochong01@outlook.com",
    description="北京航空航天大学成人教育学院API",
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask"],
    extras_require={"test": ["pytest", "coverage"]},
)
