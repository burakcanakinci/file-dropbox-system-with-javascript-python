import os
import shutil
import pathlib

import random as r
import numpy as np


file_path = os.path.abspath(pathlib.Path().absolute()) + '/'


def run():
    with open(file_path + 'out.npy', 'wb') as f:
        x = np.random.rand(50, 10)
        np.save(f, x)

    with open(file_path + 'out.npy', 'rb') as f:
        y = np.load(f)
        print(y)


if __name__ == '__main__':
    run()
