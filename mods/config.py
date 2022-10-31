from yaml import dump, full_load
from os.path import exists

config_file = "config.yaml"
input_filetypes = {"TIF":".tif"}
default_config = {"Images":{
    "format":"Keyence",
    "folders":[
        "C:/Folder1",
        "C:/Folder2",
        "C:/Folder3"
        ],
    "input_file_type":"TIF",
    "channels":{
        "CH1":None,
        "CH2":"image",
        "CH3":"phase",
        "CH4":None
        },
    }
}
    

def init_config(config_file):
    print(f"Initializing configuration file {config_file}...")
    with open(config_file, "w") as f:
        dump(default_config,f)
    print("Configuration file initialized!")
    print(f"Edit {config_file} file and re-run program.")
    input('Press "Enter" to close')
    exit()

if not exists(config_file):
    print("No configuration file found...")
    init_config(config_file)
with open(config_file,"r") as f:
    config = full_load(f)
dirs = config["Images"]["folders"]
format = config["Images"]["format"]
filetype = input_filetypes[config["Images"]["input_file_type"]]
channels = config["Images"]["channels"]
zstack = config["Images"]["zstack"]