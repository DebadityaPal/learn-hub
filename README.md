**Note: This is an Unofficial Community Project for GSoC 2021**

[![Documentation Status](https://readthedocs.org/projects/learn-hub/badge/?version=latest)](https://learn-hub.readthedocs.io/en/latest/?badge=latest)

# What is LearnHub?

LearnHub is an auxilliary tool which provides an interactive onboarding experience for the new users of [Hub](https://github.com/activeloopai/Hub).

**Reading the Documentation can be time Consuming and Boring**

Hence, we have created a library that provides interactive tutorial courses on how to get started with using Hub, right at the comfort of your local terminal.

# What is Hub?

<p align="center">
    <img src="https://github.com/activeloopai/Hub/blob/main/media/hub_logo.png"/>
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
A list of all the available courses can be acquired by running
```
python learn list
```
Linux users can remove the `python` part from both the commands.
