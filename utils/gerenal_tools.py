# coding:utf8

"""
@author: Zhangao Lu
@contact: zlu2@laurentian.ca
@time: 2021/2/24
@description:
Some tools to save and open files.
"""

import pickle
import json
import hickle
from config import config


def open_pickle(fpath):
    """
    Open pickle file
    :param fpath: string
           The file path.
    :return:
    """
    with open(fpath, "rb") as f:
        info = pickle.load(f)
    return info


def save_pickle(data, fpath):
    """
    Save pickle file.
    :param data:
           The data need to be saved.
    :param fpath:
           The file path.
    :return:
    """
    with open(fpath, "wb") as f:
        pickle.dump(data, f)


def open_json(fpath):
    """
    Open json file.
    :param fpath: string
           The file path.
    :return:
    """
    with open(fpath, 'r') as f:
        data = json.load(f)
    return data


def save_json(data, fpath):
    """
    Save json file.
    :param data:
           The data need to be saved.
    :param fpath:
           The file path.
    :return:
    """
    with open(fpath, 'w') as f:
        json.dump(data, f)


def open_text(fpath):
    """
    Open text file.
    :param fpath: string
           The file path.
    :return:
    """
    with open(fpath, "r", encoding="utf8") as f:
        return f.read()


def save_text(data, fpath):
    """
    Save text file.
    :param data:
           The data need to be saved.
    :param fpath:
           The file path.
    :return:
    """
    with open(fpath, "w", encoding='utf-8') as f:
        f.write(data)


def open_hickle(fpath):
    """
    Open hickle file.
    :param fpath: string
           The file path.
    :return:
    """
    info = hickle.load(fpath)
    return info


def save_hickle(data, fpath, iscompress=True):
    """
    Save hickle file.
    :param data:
           The data need to be saved.
    :param fpath:
           The file path.
    :param iscompress: boolean, default=True
           Choose to compress the array or not.
    :return:
    """
    if iscompress:
        hickle.dump(data, fpath, mode='w', compression='gzip')
    else:
        hickle.dump(data, fpath, mode='w')


if __name__ == '__main__':
    a = 0.00000000012334
    print(f'{a:.20f}')



