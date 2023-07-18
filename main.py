import os
import matplotlib.pyplot as plt
import pandas as pd
from tqdm.notebook import tqdm
pd.set_option("display.max_columns",None)
pd.set_option("display.max_rows",None)

directory_sizes = []
names = []

def get_size_format(b, factor=1024, suffix="B"):
    for unit in ['',"K","M","G","T","P","E","Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"

def get_directory_size(directory):
    total = 0
    try:
        for entry in os.scandir(directory):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                try:
                    total += get_directory_size(entry.path)
                except FileNotFoundError:
                    pass
    except NotADirectoryError:
        return os.path.getsize(directory)
    except PermissionError:
        return 0
    return total

def plot_pie(sizes,names, title=''):
    plt.pie(sizes, labels=names, autopct=lambda pct: f"{pct:.2f}%")
    plt.title(f"{title} Sub-directory Size")
    plt.show()
    
def exec_directory_size(root_directory):
    folder_path = root_directory
    directory_sizes.clear()
    names.clear()

    for directory in tqdm(os.listdir(folder_path)):
        directory = os.path.join(folder_path, directory)
        if os.path.isdir(directory):
            directory_size = get_directory_size(directory)
            if directory_size == 0:
                continue
            directory_sizes.append(directory_size)
            names.append(os.path.basename(directory) + ": " + get_size_format(directory_size))
