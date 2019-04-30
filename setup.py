from setuptools import setup, find_packages

with open('./README.md', 'r') as f:
    long_description = f.read()

setup(name='ural',
      version='0.8.0',
      description='A helper library full of URL-related heuristics.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/medialab/ural',
      license='MIT',
      author='Guillaume Plique, Jules Farjas, Oubine Perrin, Benjamin Ooghe-Tabanou',
      author_email='kropotkinepiotr@gmail.com',
      keywords='url',
      python_requires='>=2.7',
      packages=find_packages(exclude=['test']),
      package_data={'docs': ['README.md']},
      install_requires=[
          'phylactery>=0.2.2',
          'pycountry>=18.12.8',
          'tld>=0.9.3'
      ],
      entry_points={
          'console_scripts': ['ural=ural.cli.__main__:main']
      },
      zip_safe=True)
