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

Once Harness is cloned, you should add a profile for your user configuration [in this directory](https://github.com/RBerkheimer/harness/tree/master/harness/properties/profiles) - there is a 'standard' configuration that will be used if no configuration is specified. To add your own, just follow the standard template (or if your executables are the same as the standard, ignore this step). The .gitignore file will make sure your profile isn't propagated to the upstream if you are working as part of the development team.

The most important thing to note here are python versions! Make sure your python versions are set up correctly in the standard env or virtual env you are installing to.

We do recommend installing Harness in a virtual environment. To see how Harness can be installed in a standard virtualenv, and then validate, take a look at the [circleci config file](https://github.com/RBerkheimer/harness/blob/master/.circleci/config.yml) file.

Another good option for virtualenv installation is [pipenv](https://github.com/pypa/pipenv).
To do it with pipenv,
* Install pipenv (pip install pipenv).
* Go to your harness root directory and run 'pipenv install'
* Open your shell using 'pipenv shell'
* Run 'pip install . --upgrade' (also run this command from the project root whenever you change your project).
* To validate, run 'cd harness/src/test/processor && {python3} project_processor_test.py {circleci}' where {python3} stands for your python3 executable, and {circlci} represents your profile that you added in the 'profiles' directory (or just leave it blank if yours matches the standard profile).


Running this project_processor_test does a lot of stuff (and prints it all as output in your terminal). It

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

Once you get the results, congratulations! You've successfully installed and validated the Harness system. Now let's check the web controller/web UI!

From your project root directory, navigate to harness/src/main/controller directory. From here, run '{python3} project_controller.py {profile}', where again, your profile stands for your own profile. This will bootstrap both the flask server on port 8008 and a static resources server on port 8018. Now, **first** navigate to http://localhost:8008/test_setup - we are going to run another complete system setup to validate that our controller is hooked up to our back end. When this finishes, it should display a list of text data in a JSON map on your screen. congratulations, it loaded! Now you can navigate to http://localhost:8008/ and play with the UI.

Currently, only structures are implemented, and most of that page works with the back end. Try manipulating fields, templates, and structures, reloading the page, and you should see the persistence. **Note - we're experiencing some sort of bug with our static resource server when installed in a VirtualEnv. Currently working on this.**

If you ever want to reset the system, go ahead and navigate again to http://localhost:8008/test_setup - it will reset the system to the default test state. Enjoy!

## License

MIT Standard

Copyright 2016-2020 Ryan Berkheimer

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
