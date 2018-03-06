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

Harness currently runs on python 3, using fairly standard dependencies, and uses mongodb as the storage engine, serving on the default port. All PyPi dependencies, apart from the mongodb instance, are installed as part of the build. There are two other project packages, [mars](https://github.com/RBerkheimer/mars) and [pythoncommons](https://github.com/RBerkheimer/pythoncommons), that are also project dependencies. To see how to install these, check out the [circleci config file](https://github.com/RBerkheimer/harness/blob/master/.circleci/config.yml) and look at the 'run' section. To install mongodb, you can install the standard docker container, or download and run the binary distribution.
* Acquiring and loading mongodb
   
   * To check MongoDB Server version, Open the command line via your terminal program and execute the following command:
   `mongod --version`
   
   * Also use systemctl to check that the service has started properly.
   `sudo systemctl status mongod`
   
   * If MongoDB is not installed in your system, you can install it with the following commands:
      * Adding the MongoDB Repository: 
      `sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927`
      
     * create a list file for MongoDB: 
     `echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list`
   
      * After adding the repository details, we need to update the packages list: 
      `sudo apt-get update`
   
      * install the MongoDB package itself: 
      `sudo apt-get install -y mongodb-org`
      
      * Next, start MongoDB with systemctl: 
      `sudo systemctl start mongod`
   
      * check that the service has started properly: 
      `sudo systemctl status mongod`
   
      * enable starting MongoDB automatically when the system starts: 
      `sudo systemctl enable mongod`
      
* 	Check the versions of python installed in your system by

      * `python -V`
            (This is done to find out the default python in your system. If python3 is not set as default, 
            Place the following into ~/.bashrc or ~/.bash_aliases file
            
               alias python=python3
               
               source ~/.bash_aliases or source ~/.bashrc)
       * `python2 -V`
       * `python3 -V`
       
* Install and use pip in a local directory without root/sudo access
  
   * Download pip from an online repository : `wget https://bootstrap.pypa.io/get-pip.py `
   
   * Install the downloaded package into a local directory : 
            `python get-pip.py --user `
         This will install pip to your local directory (.local/bin). 
   * Now you may navigate to this directory (cd .local/bin) and then use pip
        or better set your $PATH variable this directory to use pip anywhere : 
            PATH=$PATH:~/.local/bin followed by source ~/.bashrc to apply the changes. 
        Gist:
        
            wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py --user
            
            cd .local/bin
            
            ./pip install <package_name> --user
            
* Make sure Python3 is installed without sudo rights. (If it is, it would 	create problems 	with pip3)  
    
   * INSTALLING PYTHON 3.6.3 WITHOUT SUDO  
    
     * Recommendation: Use pyenv. You can build and install a new (or old) version of Python by simply using then command:        
            `pyenv install 3.6.0`
    
     * Install headers needed to build 	CPythons (exotic Pythons like PyPy may have other dependencies)
             `sudo apt-get install -y build-essential libbz2-dev libssl-dev 	libreadline-dev libsqlite3-dev tk-dev`
    
     * Run the installer script (installs pyenv and some very useful pyenv plugins by the 	original author; see here for more)
         `curl -L https://raw.githubusercontent.com/yyuu/pyenv-	installer/master/bin/pyenv-installer | bash  `
    
     * Add init lines to your ~/.profile or ~/.bashrc (it mentions it at the end 	of the install script): 
      (Make sure to add this to path permanently, else add the first two lines every time you start the terminal)
             `export PATH="~/.pyenv/bin:$PATH"`
             `eval "$(pyenv init -)"`
             `eval "$(pyenv virtualenv-init -)"`
    
     * Restart your shell (close & open or exec $SHELL) or reload the profile script. (with e.g. source ~/.bashrc)
       
* Setting up an environment
    
    To not touch the system Python, which is generally a bad idea as OS-level services might be relying 
      on some specific library versions, make your own environment.
    
    Install your preferred Python version (this will download the source and build it for your 	user, no input required)
          `pyenv install 3.6.0`
    
    Make it a virtualenv so you can make others later if you want
          `pyenv virtualenv 3.6.0 general` 
    
    Make it globally active (for your user)
          `pyenv global general`
    
    Troubleshooting:      
         bash: pyenv: command not found, fish: Unknown command 'pyenv'      
      Check your $PATH, there should be one entry that ends in something like .pyenv/bin. 
         pyenv: no such command 'virtualenv'      
      If you didn't use the installer script, you likely only installed the root pyenv package. See pyenv-virtualenv for instructions to add the plugin     
      If you used the installer script, check if it shows up with pyenv commands.      
      Exit the environment using “exit” if you need to.

* Clone the three repositories: Harness, mars and pythoncommons into root of your 	system. (Make sure you have pulled the latest code)

Once Harness is cloned, you should add a profile for your user configuration [in this directory](https://github.com/RBerkheimer/harness/tree/master/harness/properties/profiles) - there is a 'standard' configuration that will be used if no configuration is specified. To add your own, just follow the standard template (or if your executables are the same as the standard, ignore this step). The .gitignore file will make sure your profile isn't propagated to the upstream if you are working as part of the development team.

The most important thing to note here are python versions! Make sure your python versions are set up correctly in the standard env or virtual env you are installing to.

We do recommend installing Harness in a virtual environment. To see how Harness can be installed in a standard virtualenv, and then validate, take a look at the [circleci config file](https://github.com/RBerkheimer/harness/blob/master/.circleci/config.yml) file. Follow all the instructions in the file.


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

Once you get the results, congratulations! You've successfully installed and validated the Harness system. 

Now let's check the web controller/web UI!

Change into your pipenv and run
	`pip install . --upgrade`
   
From your project root directory, navigate to harness/src/main/controller directory. 
From here, run '{python3} project_controller.py {profile}', where again, your profile stands for your own profile. This will bootstrap both the flask server on port 8008 and a static resources server on port 8018. 

![alt tag](https://github.com/ShriyaSalian/harness/blob/master/reference/IMG_20180306_231748.png "Root Webpage")

Now, **first** navigate to “http://localhost:8008/test_setup/standard” - we are going to run another complete system setup to validate that our controller is hooked up to our back end. 

When this finishes, it should display a list of text data in a JSON map on your screen. congratulations, it loaded! Now you can navigate to http://localhost:8008/ and play with the UI.

You can go to the structures tab and click/drag/drop on the field nodes. Dragging and dropping allows both cloning and moving.

![alt tag](https://github.com/ShriyaSalian/harness/blob/master/reference/IMG_20180306_231734.png "Structures")

Currently, only structures are implemented, and most of that page works with the back end. Try manipulating fields, templates, and structures, reloading the page, and you should see the persistence. **Note - we're experiencing some sort of bug with our static resource server when installed in a VirtualEnv. Currently working on this.**

If you ever want to reset the system, go ahead and navigate again to http://localhost:8008/test_setup - it will reset the system to the default test state. Enjoy!

## License

MIT Standard

Copyright 2016-2020 Ryan Berkheimer

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
