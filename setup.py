from setuptools import setup, find_packages

with open('./README.md', 'r') as f:
    long_description = f.read()

setup(name='ural',
      version='0.0.1',
      description='A helper library full of URL-related heuristics.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/Yomguithereal/ural',
      license='MIT',
      author='Guillaume Plique',
      author_email='kropotkinepiotr@gmail.com',
      keywords='url',
      python_requires='>=3',
      packages=find_packages(exclude=['test']),
      package_data={'docs': ['README.md']},
      install_requires=['furl>=1'],
      zip_safe=True)
