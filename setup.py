from setuptools import find_packages, setup


setup(
    name="more_common",
    version="0.1.0",
    packages=find_packages(include=["more_common", "more_common.*"]),
    install_requires=[
        "casadi>=3.5.5",
    ],
)
