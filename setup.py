from setuptools import setup, find_packages

setup(
    # Application name:
    name="brainbehavior",

    # Version number (initial):
    version="0.1",

    # Application author details:
    author="Vanessa Sochat",
    author_email="vsochat@stanford.edu",

    # Packages
    packages=find_packages(),

    # Data
    package_data = {'brainbehavior.data':['cognitiveatlas/*']},

    # Details
    url="http://www.github.com/vsoch/brainbehavior",

    license="LICENSE.txt",
    description="behavioral phenotype from cognitive assessments",

)
