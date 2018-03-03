# Harness

## Status

Version 0.0.1

[![CircleCI](https://circleci.com/gh/RBerkheimer/harness.svg?style=svg)](https://circleci.com/gh/RBerkheimer/harness)

## Introduction
Welcome to the Harness project! Harness was initially conceived as a state testing and development platform for large, complex, and evolving scientific systems.

These types of projects can consist of many distinct, independently involving packages, all required to interact together, and produce scientifically accurate and verifiable results.

It's easy to agree that this situation leads to a lot of headaches in making sure that these projects are in the states we expect them to be in. It's also easy to agree that these headaches are all but guaranteed in our current development practices, because of all of the diversity in system languages, version control systems, teams authors, project character... well, you get the idea.

Harness attempts to provide a solution to managing these dynamic systems by stereotyping common system things - treating all version control strategies as 'version control', all packages as 'components', package modules and module methods as 'functions', and state output ('evaluations') of user defined functional pipelines ('workflows').

All parts of a harness (components, functions, workflows, evaluations) are then historically versioned and tracked as a whole. These collection of state outputs are stored in well defined structures called 'mars' structures - this makes it easy to compare state output as the system which produces it changes over time.

The project has been [presented](https://www.youtube.com/watch?v=ehXGM8idcAY) at both [Earth Science Information Partners (ESIP)](http://commons.esipfed.org/node/9131) and [PyCon](https://us.pycon.org/2016/schedule/presentation/2021/), and has an available [white paper](http://commons.esipfed.org/sites/default/files/Harness_WhitePaper.pdf).

![harness](reference/Harness_PyCon.png?raw=true "Original Harness Poster - February 2016")

## Status

Harness is in active development. It has recently been moved to python 3 (originally developed in python 2). Original funding came from NOAA as part of a contract for the development of the Pairwise Homogeneity Algorithm. Funding lapsed in 2016, but the project is now being worked on as part of the Google Summer of Code 2018 program.

Current focus is on
* completing the system web UI
    * complete structures definition
    * users and user groups/login
    * harness creation
    * component selection
    * function selection
    * workflow definition
    * evaluation analytics
* improving the evaluation engine
    * improving existing python support
    * addition of support for new natively supported drivers
        * java
        * c
        * c++
        * fortran
        * R
* validating mars use and support
    * integrating mars users and user access
* adding comprehensive unit testing

## Development

A development team is forming and outlining project goals for the 2018 summer term of the GSoC project. Please contact us - we love working with motivated individuals!

## Installation

Harness currently runs on python 3, using fairly standard dependencies, and uses mongodb as the storage engine, serving on the default port. All PyPi dependencies, apart from the mongodb instance, are installed as part of the build. There are two other project packages, [mars](https://github.com/RBerkheimer/mars) and [pythoncommons](https://github.com/RBerkheimer/pythoncommons), that are also project dependencies. To see how to install these, check out the [circleci config file](https://github.com/RBerkheimer/harness/blob/master/.circleci/config.yml) and look at the 'run' section. To install mongodb, you can install the standard docker container, or download and run the binary distribution. There are many ways of acquiring and loading mongodb.

We do recommend installing Harness in a virtual environment. To see how Harness can be installed in a standard virtualenv, take a look at the [circleci config file](https://github.com/RBerkheimer/harness/blob/master/.circleci/config.yml) file. Another good option for installation is [pipenv](https://github.com/pypa/pipenv).
To do it with pipenv, just go into your harness directory, run 'pipenv install', 'pipenv shell', and 'pip install . --process-dependency-links'

Once Harness is installed, you should add a profile for your user configuration [here](https://github.com/RBerkheimer/harness/tree/master/harness/properties/profiles) - there is a 'standard' configuration that will be used if no configuration is specified. To add your own, just follow the standard template (or if your executables are the same as the standard, ignore this step). The .gitignore file will make sure your profile isn't propagated to the upstream if you are working as part of the development team.

Also, then add a config file [here](https://github.com/RBerkheimer/harness/tree/master/config) that just references the name of your profile. Again, it won't persist in the repo, but it will allow us to pass your profile name to nose to run our tests. Which brings us to the last part of this install guide - validation.

To validate your installation, run the tests using nose! From root, you can run

```
nosetests -s --tc-file **config/example_cfg.ini** where example_cfg.ini is that config file you created in the last step.
```

Running nosetests does a few things to validate the system. It

* Reads lots of property files from the properties subdirectory (check these out for yourself!)
    * header files, which define
        * our system components
        * our test functions from the components
        * our test workflows based on our test functions
        * our mars structures, which tell harness how we will be storing our data
    * records of all our definitions
* Create a new test harness
* Clones two repositories into two separate harness components
* Defines some functions on these components
* Defines several workflows against these functions
* Evaluates the test workflows
* Validates the results of all the test workflows

Once you get the results, congratulations! You've successfully installed and validated the Harness system.

There is one other part of the system that we haven't looked at, however - the web controller. You can also use the web controller to run the tests, which will then produce a nice UI for harness that is hosted locally in your browswer. Instructions for that can be found in our [development guide](https://github.com/RBerkheimer/harness/blob/master/DEVELOPMENT_README).


## License

MIT Standard

Copyright 2016-2020 Ryan Berkheimer

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
