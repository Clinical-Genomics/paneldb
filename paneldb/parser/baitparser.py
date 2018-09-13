#!/usr/bin/env python

def read_file(path_to_file):
    """Reads the bed-file and returns a list of dictionaries

    Args:
        path_to_file(): path tp temp file

    Returns:
        bait_dict_list(list): a list of dictionaries with the keys: chromosome, chr_start, chr_stop
    """
    bait_dict_list = []
    with open(pathtofile, 'r') as file:

        for line in file:
            bait = {}
            line = line.strip().split('\t')

            bait['chromosome'] = line[0]
            bait['chr_start'] = line[1]
            bait['chr_stop'] = line[2]

            bait_dict_list.append(bait)

    return bait_dict_list
