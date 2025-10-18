"""
Legacy setup.py for backward compatibility.
The project primarily uses pyproject.toml (PEP 517/518).
"""

from setuptools import setup, find_packages

setup(
    name="gpt-oss-tutorial",
    packages=find_packages(include=["src", "src.*", "examples", "examples.*"]),
)

