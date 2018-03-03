from setuptools import setup, find_packages
setup(
    name='harness',
    packages=find_packages(),
    install_requires=[
          'flask',
          'bson',
          'pythoncommons',
          'mars',
          'nose',
          'nose-testconfig'
      ],
    dependency_links=[
        "git+https://github.com/RBerkheimer/pythoncommons.git#egg=pythoncommons-0.0.1",
        "git+https://github.com/RBerkheimer/mars.git#egg=mars-0.0.1"
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
        "License :: MIT Standard",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic"])
