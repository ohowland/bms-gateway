from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name='bms-gateway', 
    version='0.1.0',
    author="Owen Edgerton",
    author_email="author@example.com",
    description="CANbus translation gateway framework",
    long_description=long_description,
    url="https://www.howlandedgerton.com/bms-gateway",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Howl & Edgerton Software License",
        "Operating System :: Debain 10",
        ],
    python_requires='>=3.6',
)

