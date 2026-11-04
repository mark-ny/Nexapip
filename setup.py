from setuptools import find_packages, setup

setup(
    name="nexapip",
    version="0.1.0",
    description="Research and paper-trading framework",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=["pandas>=2.0"],
    entry_points={"console_scripts": ["nexapip=nexapip.cli:main"]},
)
