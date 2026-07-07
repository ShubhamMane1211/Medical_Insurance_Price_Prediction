from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = "-e ."


def get_requirements(file_path: str) -> List[str]:
    """
    Read requirements.txt and return a list of package requirements.
    """
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements


setup(
    name="medical-insurance-price-prediction",
    version="1.0.0",
    author="Your Name",
    author_email="you@example.com",
    description="A production-ready ML web app that predicts medical insurance charges",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
)
