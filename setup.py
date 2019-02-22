from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='neuralFrame',
    version='0.1',
    author='Jonathan D. Mutal',
    author_email='Jonathan.Mutal@unige.ch',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joni115/neuralFrame",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
)
