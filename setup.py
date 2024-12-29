from setuptools import setup, find_packages

setup(
    name="line-integral-convolutions",
    version="1.0.0",
    url="https://github.com/AstroKriel/line-integral-convolutions/tree/main",
    description="A script showcasing my implementation for computing line integral convolution.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Neco Kriel",
    author_email="neco.kriel@anu.edu.au",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["numpy", "matplotlib", "scipy", "numba", "scikit-image"],
)
