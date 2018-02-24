from setuptools import setup, find_packages
setup(
    name='harness',
    packages=find_packages(),
    install_requires=[
          'pymongo',
          'flask',
          'simplejson',
          'geojson',
          'pythoncommons',
          'mars'
      ],
    include_package_data=True,
    version='0.0.1',
    description='The Harness Project',
    author='Ryan Berkheimer',
    author_email='rab25@case.edu',
    url='https://github.com/RBerkheimer/harness',
    classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic"])
