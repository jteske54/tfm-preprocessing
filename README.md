# TractionsForAll Pre-Processing

*Author:* Jacob Teske

*Language:* Python

*Created:* 2022-09-27

*Modified:* 2022-10-26

## Configuration File

When the program is run for the first time, or whenever no configuration file is found, a `config.yaml` file will be created in the same directory as the program. The contents of the default file will be found as below:

```yaml
Images:
  channels:
    CH1: null
    CH2: image
    CH3: phase
    CH4: null
  folders:
  - C:\Folder1
  - C:\Folder2
  - C:\Folder3
  format: Keyence
  input_file_type: TIF
```

### Channels

Change the channels to match the channels used to image. The channel used to image the beads should be labelled as `image`, and the channel used to image the cells (CellMask, DiI, phase contrast, etc.) should be labelled as `phase`. Any unused channels can be set as `null`. *NOTE: no channel values can be left blank. They must be set to `null`, or the channel key (CH1:, CH2:, etc.) must be deleted completely.*

### Folders

Here you will put the folders that you want the script to recurse through. They can be in the default format your OS uses, so you can simply copy-and-paste from an explorer window.

### Format

Currently, the only format offered is `Keyence`, so that can be left default.

### Input File Type

The image filetype used. (i.e. `TIF`, `PNG`, `JPEG`, etc.)

# Setting up Python environment

This program was written using Python `3.10.7`. I have not tested other versions. They may or may not work.

I recommend using a 'virtual enviroment' (venv) when running this program. To create a virtual environment with Python, in the folder that contains `tfm.py`, run:

`python -m venv venv`

Then, activate the venv by running:
*On Mac/Linux:*

`source venv/bin/activate`

*On Windows:*

`venv\Scripts\activate`

You can then install the required modules by running:

`python -m pip install -r requirements.txt`

The environment should now be ready to run the program.

## Running the program

To run the program after setting up the config file, in a terminal/command prompt, run:

`python tfm.py`

The program should start to run. In the terminal window, you should see progress bars for each step of the processing. When the processing has finished, `Done!` should be printed on the screen.

Depending on the storage location of your images (hard drive, flash drive, network drive, etc.) and how many images you have, processing should take anywhere from a couple of minutes to an hour.