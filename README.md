**Note: This is an Unofficial Community Project for GSoC 2021**

[![Documentation Status](https://readthedocs.org/projects/learn-hub/badge/?version=latest)](https://learn-hub.readthedocs.io/en/latest/?badge=latest)

# What is LearnHub?

LearnHub is an auxilliary tool which provides an interactive onboarding experience for the new users of [Hub](https://github.com/activeloopai/Hub).

**Reading the Documentation can be time Consuming and Boring**

Hence, we have created a library that provides interactive tutorial courses on how to get started with using Hub, right at the comfort of your local terminal.

# What is Hub?

<p align="center">
    <img src="https://camo.githubusercontent.com/4747ade63cbe1ec71dbaee37546c669fa0ccca7fb05b8fdeb5c42a1cdc0a1266/68747470733a2f2f7777772e6c696e6b706963747572652e636f6d2f712f6875625f6c6f676f2d312e706e67"/>
</p>

**The fastest way to access and manage datasets for PyTorch and TensorFlow**

Hub provides fast access to the state-of-the-art datasets for Deep Learning, enabling data scientists to manage them, build scalable data pipelines and connect to Pytorch and Tensorflow.

# Getting Started

### Installing

Follow these steps to install and start using LearnHub.

```
git clone https://github.com/DebadityaPal/learn-hub
cd learn-hub
pip install -e .
```

### Upgrade

If you want to upgrade your current installation of LearnHub, follow these steps.

```
cd learn-hub
git pull origin main
```

# Running a Course
If you want to run a course you simply need to run the following command on the console.
```
python learn run courses/<course_name>
```
for example
```
python learn run "courses/Getting started with Hub"
```
A list of all the available courses can be acquired by running
```
python learn list
```
Linux users can remove the `python` part from both the commands.


# GSoC Checklist
 - [x] Make a Basic YAML parser to read course files.
 - [x] Make a general course engine to provide content on the terminal.
 - [x] Make General Snippet class which will be extended later.
 - [x] Make Text Snippet Class
 - [x] Make MCQ Snippet Class
 - [x] Make Code Snippet Class
 - [x] Add Automated Documentation Pipeline
 - [x] Add Courses in the library after incorporating team feedback.
 - [x] Stretch: Add colors to make courses visually appealing.
