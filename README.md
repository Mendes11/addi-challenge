# Technical Challenge

## Objective

The aim of this project is to automate the validation process of **Leads** to 
be converted into **Prospects**

## Architecture

A Hexagonal architecture was used to create this project.
Each service is considered a `Core` that has it's `Input Ports` and 
`Output Ports`. The interface of all services can be found at `services.
service_ports` package while the `Output Ports` are in a `ports` package 
inside each service's package.


## System Flow

In order to validate a Lead, the user should trigger an action at the 
`Prospects Service` that will trigger an action in validators `National ID 
Validator Service` and `Judicial Records Validator Service`.

After each validator above finishes it's task, it triggers the `Prospect 
Validator Service` that stores the validations results until all 
validations are finished. At this time, it will compute the score of the 
request's Lead and if it is higher than 60, the Lead will be considered a 
valid lead.

The final step is the trigger of `Prospects Service` when the `Prospect 
Validator` finishes the validation, containing the information about the 
whole validation process. If the `Lead` is considered valid, then it is 
registered as a `Prospect` and persisted. Also, the `Lead` will be updated 
to have the `converted` attribute True.

## Mock Implementation

In order to test the architecture and services, along with unit tests, a mock 
implementation of the system was made by creating `Adapters` to handle all 
data internally (Storaging, API Calls and Event Subscriptions).

You can run `python main.py` in order to check the code in action.

