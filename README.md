# drawbot

![Tests](https://github.com/ejbosia/drawbot/actions/workflows/tests.yml/badge.svg)

**THIS IS A WORK IN PROGRESS!!! TESTS ARE NOT COMPREHENSIVE YET**

This repository works with the "drawbot" project, which is a simple cartesian drawing robot. The program takes in binary images and "fills" them using different fill techniques. An eventual goal is to branch into more generic images, including color.

The code is written in Python.

**It is still in progress**

Right now, the goal is to implement Connected Fermat Spirals from my other repository.

## Fill Techniques
 - Outline Fill
 - Rectilinear fill
 - Spiral fill
 - *CFS fill*

## Shading Techniques
 - *in progress*


## Installation Instructions

```bash
pip3 install -r requirements.txt
```

## Exectuion Instructions
Running the main.py file provides different command line options for execution.

```bash
python3 main.py "files/test.png" -z 1 -p
```
