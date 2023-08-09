# onmyoji_treasure

[//]: # (## Description)

Onmyoji script based on [OpenCV](https://opencv.org/) helps players reduce meaningless repetitive operations, and can
also be used by novices
to learn Python.

### Features

* Realm Raid
    * Rename the Shikigami to '小绿' to enable auto-marking.
        * It is recommended to place it in the second or third position to avoid blocking the green mark.
        * If you don't need this method, please ignore it.
    * Individual
        * Retreats 2 by default.
        * The last realm should be unbroken.
    * Guild
* Sougenbi Challenge
    * Support Automatically empty realm raid passes.
        * Consume the passes first.
        * Preset two independent lineups.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Python 3.6](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3114/)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install -r requirements.txt
```

## Usage

Before running the script:

* Set emulator resolution to **1024 x 576**, non-minimizable.
* Lock the lineup.

```bash
python main.py
```

After obtaining admin rights, the following will be printed:

![example](https://raw.githubusercontent.com/ephanoco/onmyoji_treasure/master/blob/example.png)

Place the cursor in the window as prompted. After the countdown ends, the window handle and name will be printed:

![example_02](https://raw.githubusercontent.com/ephanoco/onmyoji_treasure/master/blob/example_02.png)

After confirming that the window is correct, select the mode.

## Support

If you encounter bugs or have suggestions, please raise issues.

## License

[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)

## Project status

Try using Machine learning on the Demon Parade.