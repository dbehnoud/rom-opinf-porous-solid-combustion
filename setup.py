from setuptools import setup, find_packages

setup(
    name="rom-uq-combustion",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy", "pandas", "matplotlib", "scipy", "opinf"
    ],
    author="Your Name",
    description="Reduced-order modeling and UQ for porous solid combustion using OpInf.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
)