from setuptools import setup, find_packages

setup(
    name="benchforge",
    version="1.0.0",
    description="BenchForge: Open Scientific Evidence Infrastructure for the Agentic Era",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "benchforge=skills.benchforge.cli.main:main",
        ],
    },
)
