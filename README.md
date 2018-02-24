# Harness

## Introduction
Welcome to the Harness project! Harness was initially conceived as a state testing and development platform for large, complex, and evolving scientific systems.

These types of projects can consist of many distinct, independently involving packages, all required to interact together, and produce scientifically accurate and verifiable results.

It's easy to agree that this situation leads to a lot of headaches in making sure that these projects are in the states we expect them to be in. It's also easy to agree that these headaches are all but guaranteed in our current development practices, because of all of the diversity in system languages, version control systems, teams authors, project character... well, you get the idea.

Harness attempts to provide a solution to managing these dynamic systems by stereotyping common system things - treating all version control strategies as 'version control', all packages as 'components', package modules and module methods as 'functions', and state output ('evaluations') of user defined functional pipelines ('workflows').

All parts of a harness (components, functions, workflows, evaluations) are then historically versioned and tracked as a whole. These collection of state outputs are stored in well defined structures called 'mars' structures - this makes it easy to compare state output as the system which produces it changes over time.

The project has been presented at both Earth Science Information Partners (ESIP) and PyCon, and has an available white paper.

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

A development team is forming and outlining project goals for the 2018 summer term of the GSoC project.

## License

MIT Standard

Copyright 2016-2020 Ryan Berkheimer

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
