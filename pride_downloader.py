import os 
import sys

import ppx
import random
import json

# function that queries a random sample of data from PRIDE
# 'query' denotes the list of pride id's, 'n_prides' denotes the number of pride id's to query
# 'organism' denotes the species tag. Default is human.

def pride_downloader(query, n_prides, organism='human'):

    i = 0   # indexer for the query list
    count = 0   ### For ever successful raw download, counter will incrememntally increase

    while count < n_prides:

        proj = ppx.find_project(query[i], repo="PRIDE", timeout=10)
        organism_list = [ table['name'] for table in proj.metadata['organisms']]

        if (len(organism_list) == 1) and (organism in organism_list[0]) == True:
            
            # ppx can't query all pride id's successfully
            # the try block below prevents the function from halting when errors occur
            try:
                path = "./data/" + query[i]
                os.mkdir(path)
                proj.local = path
                proj.download("README.txt")

                with open(path + "/{}_meta.json".format(query[i]), "w") as outfile:
                    json.dump(proj.metadata, outfile)

                raw_dls = proj.remote_files("*.raw")[0]
                proj.download(raw_dls)

                count+=1

            except:
                pass
        
        i += 1

if __name__ == '__main__':
    # listing all pride id's and setting up parameters for the main function
    db = ppx.pride.list_projects()
    random.shuffle(db)
    n_prides = int(sys.argv[1])

    pride_downloader(db, n_prides, organism='human')
