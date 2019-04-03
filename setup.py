import setuptools

with open("README.md", "r") as fh:
    long_desc = fh.read()

setuptools.setup(
    name='qrandom',
    version='1.0.0',
    scripts=['qrandom','vm'],
    author="Noah Wood",
    author_email="",
    description="Shrodingers Random Number Generator",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/NoahGWood/QRandom",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GPLv3 License",
        "Operating System :: Unix",
        "Operating System :: Linux",
        "Operating System :: BSD",
	],
    )
