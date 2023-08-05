# onmyoji_treasure

[//]: # (## Description)

An Onmyoji script based on [OpenCV](https://opencv.org/) to help players avoid meaningless repetitive operations and for
beginners to learn
Python.

### Features

* Realm Raid
    * In some modes, it is automatically marked by default. Just rename the Shikigami that needs to be marked
      as '小绿'.
      It is recommended to place it in the second or third position to avoid blocking the green mark. If you do not need
      this
      function, please ignore it.
    * Individual Realm Raid retreats 2 by default, before running the script, please make sure to manually retreat 4
      first every week and the last realm is unraided.
* Sougenbi Challenge
    * Support Automatically empty realm raid passes
        * Please consume the extra realm raid passes first.
        * Prepare two independent lineups in advance.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Python 3.6](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3114/)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install -r requirements.txt
```

## Usage

**_NOTE:_** Before running the script, make sure the emulator resolution is 1024 x 576, Sticky is turned on, and the
lineup is
locked.

```bash
python main.py
```

After obtaining admin rights, you will see bash output the following:

![example](https://raw.githubusercontent.com/ephanoco/onmyoji_treasure/master/blob/example.png)

## Support

Currently only some features are supported, users are welcome to raise issues to add new
features.

## License

[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)

## Project status

Currently, the Demon Parade module is trying to use Machine learning to apply.