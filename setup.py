from setuptools import setup, find_packages


setup(
    name="battlefield",
    description="Small terminal game that uses wwapi for sounds",
    version="1.0",
    packages=find_packages(),
    author="Francis Gauthier",
    author_email="fgauthier@audiokinetic.com",
    install_requires=["kivy"],
    python_requires=">=3.8",
)
