from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(this_directory, "requirements.txt")) as f:
    requirements = f.readlines()

setup(
    name="learnhub",
    version="1.0",
    description="Interactive Onboarding Enviroment",
    scripts=["learn"],
    packages=find_packages(),
    install_requires=requirements,
)
