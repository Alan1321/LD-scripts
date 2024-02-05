import os
import earthaccess as ea
import random

def make_directory(path):
    # path = os.path.join(base_path, directory_name)
    if os.path.exists(path) == False:
        os.mkdir(path)
        return True
    return False

#pull datasets from EDS directly
def download_data(doi, download_path, date_start, date_end):
    auth = ea.login(persist=True) # use 'interactive' strategy the first time to log in
    DAAC2 = 'GHRC_DAAC'
    #doi of dataset
    # doi = "10.5067/LIS/LIS/DATA301"
    
    # step2: get links #
    results2 = ea.search_data(
        doi=doi,
        cloud_hosted=True,
        temporal=(date_start, date_end)
    )
    
    # data_link list
    https_links2 = []  # external link, todo: find ways to directly access data using external link

    for granule in results2:
        https_links2.extend(granule.data_links(access="on_prem"))

    https_links2 = [file for file in https_links2 if file.endswith(".nc.gz") or file.endswith(".nc") or file.endswith(".dat.gz")]#only select .nc files
    file_count = len(https_links2)

    if file_count != 0:
        # os.mkdir(folder_name)#define folder to store data
        ea.download(https_links2, download_path)#download_data
        print(f'Data downloaded on folder: {download_path}')
        
    #unzip the .gz files
    # filename = unzip(os.path.join(os.getcwd(), folder_name))
    # return file_count, folder_name, filename