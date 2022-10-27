# TractionsForAll Pre-Processing

*Author:* Jacob Teske

*Language:* Python

*Created:* 2022-09-27

*Modified:* 2022-10-26

## Configuration File

When the program is run for the first time, or whenever no configuration file is found, a `config.yaml` file will be created in the same directory as the program. The contents of the default file will be found as below:

```
Images:
  channels:
    CH1: null
    CH2: image
    CH3: phase
    CH4: null
  folders:
  - C:/Folder1
  - C:/Folder2
  - C:/Folder3
  format: Keyence
  input_file_type: TIF
  recursive: true
```

