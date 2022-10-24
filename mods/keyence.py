import mods.file_handling as fh
from tqdm import tqdm

def keyence():
    files = fh.get_images()
    print(f"Found {len(files)} images.")
    fh.remove_nonimages()
    fh.remove_overlay()
    fh.keep_best_image()
    fh.convert_greyscale()
    images = fh.get_images()
    files, subs = fh.get_files()
    with tqdm(total=len(images), desc="Moving images to parent directory...") as pbar:
        for image in images:
            fh.move_to_parent_folder(image)
            pbar.update(1)
    fh.remove_extra_directories(subs)
    fh.rename_images()
    fh.align()
    