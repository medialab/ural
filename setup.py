from setuptools import setup, find_packages

with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name="ural",
    version="0.39.0",
    description="A helper library full of URL-related heuristics.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/medialab/ural",
    license="MIT",
    author="Guillaume Plique, Jules Farjas, Oubine Perrin, Benjamin Ooghe-Tabanou, Martin Delabre, Pauline Breteau, Jean Descamps, Béatrice Mazoyer, Amélie Pellé, Laura Miguel",
    author_email="guillaume.plique@sciencespo.fr",
    keywords="url",
    python_requires=">=2.7",
    packages=find_packages(exclude=["scripts", "test"]),
    package_data={"docs": ["README.md"]},
    install_requires=[],
    extras_require={":python_version<'3.8'": ["typing_extensions"]},
    zip_safe=True,
)
