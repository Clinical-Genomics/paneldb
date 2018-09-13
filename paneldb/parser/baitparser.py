#!/usr/bin/env python

def read_file(pathtofile):
    """Reads the bed-file and returns a dictionary containing the three first columns of file

    Keyword arguments:
    pathtofile -- path to bed-file
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

