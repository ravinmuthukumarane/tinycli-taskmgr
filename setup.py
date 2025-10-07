from setuptools import setup, find_packages

setup(
    name="tinytask",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer[all]>=0.12.3",
        "rich>=13.7.1",
    ],
    entry_points={
        "console_scripts": [
            "task=tinytask.cli:app",
        ],
    },
    author="Your Name",
    description="A tiny CLI task manager for personal productivity",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
)
