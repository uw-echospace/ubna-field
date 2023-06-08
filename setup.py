from setuptools import find_packages, setup

# Dependencies
with open("requirements-dev.txt") as f:
    requirements = f.readlines()
INSTALL_REQUIRES = [t.strip() for t in requirements]

setup(
    name="Union Bay Bats",
    description="Union Bay Bats Passive Acoustic Monitoring Repository",
    url="https://github.com/uw-echospace/union-bay-bats",
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
)