# Harness

## Introduction
Welcome to the Harness project! Harness was initially conceived as a state testing and development platform for large, complex, and evolving scientific systems.

These types of projects can consist of many distinct, independently involving packages, all required to interact together, and produce scientifically accurate and verifiable results.

It's easy to agree that this situation leads to a lot of headaches in making sure that these projects are in the states we expect them to be in. It's also easy to agree that these headaches are all but guaranteed in our current development practices, because of all of the diversity in system languages, version control systems, teams authors, project character... well, you get the idea.

Harness attempts to provide a solution to managing these dynamic systems by stereotyping common system things - treating all version control strategies as 'version control', all packages as 'components', package modules and module methods as 'functions', and state output of user defined functional pipelines, or 'workflows'. All these things are then historically versioned and tracked as a whole using comparable state output as individual parts and pieces. These collection of state outputs are called 'evaluations', and are stored in well defined structures called 'mars' structures - this makes it easy to compare state output as the system which produces it changes over time.

## 
