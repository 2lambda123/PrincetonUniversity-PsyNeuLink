# PsyNeuLink

PsyNeuLink is a block modeling system for cognitive neuroscience.
It is open source, and meant to be extended

### Contributors
    - Jonathan D. Cohen, Princeton Neuroscience Institute, Princeton University
    - Peter Johnson, Princeton Neuroscience Institute, Princeton University
    - Bryn Keller, Intel Labs, Intel Corporation
    - Sebastian Musslick, Princeton Neuroscience Institute, Princeton University
    - Amitai Shenhav, Cognitive, Linguistic, & Psychological Sciences, Brown University
    - Michael Shvartsman, Princeton Neuroscience Institute, Princeton University
    - Ted Willke, Intel Labs, Intel Corporation
    - Nate Wilson, Princeton Neuroscience Institute, Princeton University 

### License

    Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
         http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
    on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and limitations under the License.

## Installation

Documentation is available at https://princetonuniversity.github.io/PsyNeuLink/

Right now, PsyNeuLink is in an alpha state and is not available through pypi/pip. Instead, you can clone the github repo [here](https://github.com/PrincetonUniversity/PsyNeuLink). Clone the master branch. Download the package with the green "Clone or download" button on the right side of the page and "Download ZIP."

Alternatively, if you are familiar with git, the directory can be cloned as usual through the terminal.
Note: The repo is currently private, so if the link leads to a dead page, reach out to one of the developers to get acccess.

PsyNeuLink is compatible with any version of python 3, but the tutorial requires a 3.5 installation with the latest versions of IPython, jupyter, and matplotlib installed.

To install the package, navigate to the cloned directory in a terminal, switch to your preferred python3 environment, then run the command __"pip install ."__ (make sure to include the period and to use the appropriate pip/pip3 command for python 3). All prerequisite packages will be automatically added to your environment.

There is a tutorial available to introduce the basic syntax and usage of PsyNeuLink. To access it, make sure you fulfill the requirements mentioned above, then run the terminal command "jupyter notebook" from the root PsyNeuLink directory. Once the directory opens in your browser, click on "PsyNeuLink Tutorial.ipynb"

If you have trouble installing PsyNeuLink, or run into other problems, please contact psyneulinkhelp@princeton.edu. 

## Purpose

To provide an environment for implementing models of mind/brain function that is modular, customizable and extensible.  
It does this in a manner that:

- is computationally general
- adheres as closely as possible to the insights and design principles that have been learned in CS
    (e.g., function-based, object-oriented, programming)
- expresses (the smallest number of) "commitments" that reflect general principles of how
    the brain/mind is organized and function, without committing to any particular model or theory
- expresses these commitments in a form that is powerful, easy to use, and familiar to cognitive neuroscientitsts
- allows models to be simply and flexibly implemented, using a minimum of coding that provides 
     seamless interaction among disparate components that can vary in their:
     + time-scale of operation
     + granularity of representation and function
- encourages users to think about processing in a "mind/brain-like" way,
     while imposing as few constraints as possible on what they can implement or ask their model to do
- provides a standard environment for model comparison, sharing, and integration  

## Functional Architecture

PsyNeuLink is written in Python, and conforms to the syntax and (most of the) coding standards for the language.
It provides a framework with the following structural components, as well as a set of methods for creating,
customizing and executing them:

- System:
     set of (potentially interacting) processes, that can be managed by a “budget” of control and trained.

     - Process: 
         takes an input, processes it through an ordered list of mechanisms and projections, and generates an output.
    
         + Mechanism: 
             transforms an input representation into an output representation.
             Parameters determine its operation, under the influence of projections.
             There are three primary types:
             
             + ProcessingMechanism:
                  aggregates the inputs it receives from other mechanisms or the input to a process or system, 
                  transforms them in some way, and provides the result either as input to other mechanisms and/or 
                  to the output of a process or system.
             
             + ControlMechanism
                  evaluates the output of one or more other mechanisms, and uses this to modify the parameters of those
                  or other mechanisms.

             + MonitoringMechanism
                   monitors the output of one or more other mechanisms, compares these to a target value,
                   and generates an error signal used for learning.
    
         + Projection: 
             takes the output of a mechanism, possibly transforms it, and uses it to determine the operation of 
             another mechanism. There are three primary types:
    
             + MappingProjection:
                takes the output of a mechanism, transform it as necessary to be usable by a receiver mechanism,
                and provides it as input to that receiver mechanism.
    
             + ControlProjection:
                 takes an allocation (scalar) (usually the output of a ControlMechanism) 
                 and uses it to modulate the parameter(s) of a mechanism.
    
             + LearningProjection:
                 takes an error signal (scalar or vector, usually the output of a Monitoring Mechanism) 
                 and uses it to modulate the parameter of a projection (usually the matrix of a MappingProjection).
                 
             [+ GatingProjection — Not yet implemented
                 takes a gating signal source and uses it to modulate the input or output state of a mechanism.
