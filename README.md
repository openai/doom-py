# doom_py

[![Build Status](https://travis-ci.org/openai/doom-py.svg?branch=master)](https://travis-ci.org/openai/doom-py)

Python wrappers for [ViZDoom](http://vizdoom.cs.put.edu.pl/).
Contains a modified version of the [bleeding-edge](https://github.com/Marqt/ViZDoom/tree/5749d0a49dc6679cc7583b86e5c1861163644c39)
ViZDoom source code.

###Requirements

* CMake 3.0+
* Make
* GCC 4.6+
* Boost Libraries
* SDL 2.0.2
* Python with Numpy

To install dependencies on OS X via Brew, type

```brew install cmake boost boost-python```

To install dependencies on Ubuntu, type

```apt-get install -y python-numpy cmake zlib1g-dev libjpeg-dev libboost-all-dev gcc libsdl2-dev wget unzip```
