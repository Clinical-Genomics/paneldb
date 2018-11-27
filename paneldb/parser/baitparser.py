#!/usr/bin/env python

def baits(path_to_file, created_baitset_id=None, build='GRCh37'):
    """Reads the bed-file and returns a list of dictionaries

    Args:
        path_to_file(): path tp temp file

    Returns:
        bait_dict_list(list): a list of dictionaries with the keys: chromosome, chr_start, chr_stop
    """
    bait_dict_list = []
    with open(path_to_file, 'r') as file:
        for line in file:
            bait = {}
            line = line.strip().split('\t')
            bait['chromosome'] = line[0]
            bait['chr_start'] = line[1]
            bait['chr_stop'] = line[2]
            if created_baitset_id:
                bait['baitset'] = [created_baitset_id]

            #create a unique id for the bait:
            # id looks like this: chr_start_stop_build
            bait['_id'] = bait['chromosome']+"_"+bait['chr_start']+"_"+bait['chr_stop']+"_"+build

            bait_dict_list.append(bait)

    return bait_dict_list
