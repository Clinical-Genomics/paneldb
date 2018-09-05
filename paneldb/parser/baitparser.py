#!/usr/bin/env python



def read_file(pathtofile):

    bait_dict_list = []
    with open(pathtofile, 'r') as file:
        #Open the bed-file and strip of whitespace and return the lines as lists
        for line in file:
            bait = {}
            line = line.strip().split('\t')

            bait['chromosome'] = line[0]
            bait['chr_start'] = line[1]
            bait['chr_stop'] = line[2]

            bait_dict_list.append(bait)

    return bait_dict_list

