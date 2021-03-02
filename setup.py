from setuptools import setup, find_packages

with open('./README.md', 'r') as f:
    long_description = f.read()

setup(name='ural',
      version='0.26.1',
      description='A helper library full of URL-related heuristics.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/medialab/ural',
      license='MIT',
      author='Guillaume Plique, Jules Farjas, Oubine Perrin, Benjamin Ooghe-Tabanou, Martin Delabre, Pauline Breteau, Jean Descamps',
      author_email='guillaume.plique@sciencespo.fr',
      keywords='url',
      python_requires='>=2.7',
      packages=find_packages(exclude=['scripts', 'test']),
      package_data={'docs': ['README.md']},
      install_requires=[
        'phylactery>=0.2.2',
        'pycountry>=18.12.8,<19',
        'tld>=0.12.1,<1'
      ],
      zip_safe=True)
