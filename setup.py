from setuptools import find_packages, setup

setup(
    name="gh-repo-sweeper",
    version="0.1.0",
    description="A CLI utility to list, search, and delete GitHub repositories.",
    author="kuhlekt1v",
    packages=find_packages(),
    install_requires=[
        "PyGithub>=1.59",
        "keyring>=24.0.0",
    ],
    entry_points={
        "console_scripts": [
            "gh-repo-sweeper=gh_repo_sweeper.cli:main",
        ],
    },
    python_requires=">=3.8",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
