from os import rename, walk, path, remove, sep
import mods.config as config
import mods.image_handling as ih
from shutil import rmtree
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from tqdm import tqdm

def convert_greyscale():
    images = get_images()
    with tqdm(total=len(images), desc="Coverting images to greyscale...") as pbar:
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = []
            for image in images:
                futures.append(executor.submit(ih.convert_greyscale, image))
            for future in as_completed(futures):
                pbar.update(1)

def get_images() -> list:
    filelist = []
    for dir in config.dirs:
        for root, subs, files in walk(dir):
            files.sort()
            for file in files:
                if config.filetype in file:
                    filelist.append(path.join(root,file))
    return filelist

def get_files():
    file_list = []
    dir_list = []
    for dir in config.dirs:
        for root, subs, files in walk(dir):
            dir_list.append(path.normpath(root))
            for file in files:
                file_list.append(path.normpath(path.join(root, file)))
    return file_list, dir_list

def remove_nonimages() -> int:
    files, dirs = get_files()
    with tqdm(total=len(files), desc="Removing non-images...") as pbar:
        for file in files:
            if config.filetype not in file:
                remove(file)
            pbar.update(1)
    return 0

def move_to_parent_folder(file: str) -> int:
    file = path.normpath(file)
    split = file.split(sep)
    image = split.pop()
    split.pop()
    newpath = "/".join(split)
    newfile = path.normpath(path.join(newpath, image))
    rename(file, newfile)
    return 0

def remove_overlay() -> int:
    files = get_images()
    with tqdm(total=len(files), desc="Removing overlay images...") as pbar:
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = []
            for file in files:
                if "Overlay" in file:
                    futures.append(executor.submit(remove, file))
                else:
                    pbar.update(1)
            for future in as_completed(futures):
                pbar.update(1)
    return 0

def rename_images() -> int:
    bar_max = get_images()
    with tqdm(total=len(bar_max), desc="Renaming images...") as pbar:
        for dir in config.dirs:
            for root, subs, files in walk(dir):
                counts = {"ch1":1,"ch2":1,"ch3":1,"ch4":1}
                if bool(files):
                    files.sort()
                    for file in files:
                        if "CH1" in file:
                            rename(path.normpath(path.join(root,file)),path.normpath(path.join(root,config.channels["CH1"] + str(counts["ch1"]).zfill(2) + ".tif")))
                            counts["ch1"] += 1
                        if "CH2" in file:
                            rename(path.normpath(path.join(root,file)),path.normpath(path.join(root,config.channels["CH2"] + str(counts["ch2"]).zfill(2) + ".tif")))
                            counts["ch2"] += 1
                        if "CH3" in file:
                            rename(path.normpath(path.join(root,file)),path.normpath(path.join(root,config.channels["CH3"] + str(counts["ch3"]).zfill(2) + ".tif")))
                            counts["ch3"] += 1
                        if "CH4" in file:
                            rename(path.normpath(path.join(root,file)),path.normpath(path.join(root,config.channels["CH4"] + str(counts["ch4"]).zfill(2) + ".tif")))
                            counts["ch4"] += 1
                        pbar.update(1)
                    rename(path.join(root,"image" + str(max(counts.values())-1).zfill(2) + ".tif"),path.join(root,"trypsin.tif"))
                    rename(path.join(root,"phase" + str(max(counts.values())-1).zfill(2) + ".tif"),path.join(root,"phnocells.tif"))

def keep_best_image() -> int:
    max, max2 = get_files()
    with tqdm(total=len(max2), desc="Processing z-stacks...") as pbar:
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for dir in config.dirs:
                for root, subs, files in walk(dir):
                    if bool(files):
                        args = (root, files)
                        futures.append(executor.submit(keep_best_image2, *args))
                    else:
                        pbar.update(1)
                for future in as_completed(futures):
                    pbar.update(1)
    return 0

def keep_best_image2(root, files):
    ch = [[],[],[],[]]
    for file in files:
        if "CH1" in file:
            ch[0].append(path.normpath(path.join(root,file)))
        if "CH2" in file:
            ch[1].append(path.normpath(path.join(root,file)))
        if "CH3" in file:
            ch[2].append(path.normpath(path.join(root,file)))
        if "CH4" in file:
            ch[3].append(path.normpath(path.join(root,file)))
    for c in ch:
        if bool(c):
            sobels = {}
            for image in c:
                sobels[image] = ih.sobel(image)
            sorted_tuples = sorted(sobels.items(), key=lambda item: item[1])
            delete_items = sorted_tuples[:-1]
            for item in delete_items:
                remove(item[0])


def remove_extra_directories(dir_list: list) -> int:
    with tqdm(total=len(dir_list), desc="Removing extra directories...") as pbar:
        for dir in dir_list:
            if "T0" in dir:
                rmtree(dir)
            pbar.update()
    return 0

def align():
    bar_max = get_images()
    with tqdm(total=len(bar_max), desc="Aligning images...") as pbar:
        with ProcessPoolExecutor(max_workers=4) as executor:
            futures = []
            for dir in config.dirs:
                for root, subs, files in walk(dir):
                    if bool(files):
                        for file in files:
                            if "image" in file:
                                if "01" not in file:
                                    ref = path.normpath(path.join(root,"image01.tif"))
                                    mov = path.normpath(path.join(root,file))
                                    ph_file = "phase" + file[-6:]
                                    ph = path.normpath(path.join(root,ph_file))
                                    args = (ref, mov, ph)
                                    futures.append(executor.submit(ih.align_images, *args))
                                if "01" in file:
                                    pbar.update(2)
                            elif "trypsin" in file:
                                ref = path.normpath(path.join(root,"image01.tif"))
                                mov = path.normpath(path.join(root,file))
                                ph = path.normpath(path.join(root,"phnocells.tif"))
                                args = (ref, mov, ph)
                                futures.append(executor.submit(ih.align_images, *args))
            for future in as_completed(futures):
                pbar.update(2)