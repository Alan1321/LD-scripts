import os
from utils import make_directory, download_data

#consts
BASE_PATH = '/home/ubuntu/'
BASE_PATH = "/home/asubedi/"

#paths
nalma_input_file_path = f"{BASE_PATH}data/NALMA_input"
glm_input_file_path = f"{BASE_PATH}data/GLM_input"

#make data and nalma_input folder if it doesn't already exists
make_directory(BASE_PATH + '/data/')
make_directory(nalma_input_file_path)
make_directory(glm_input_file_path)

def download_nalma_or_glm(which_dataset, date_start, date_end):
    if which_dataset.lower() == 'nalma':
        # downloading nalma dataset to the path below
        print("Downloading NALMA...")
        nalma_doi = "10.5067/NALMA/DATA101"
        # date_start, date_end = "2020-01-01","2020-01-02"
        download_data(nalma_doi, nalma_input_file_path, date_start, date_end)
    else:
        #downloading glm dataset
        print("Downloaindg GLM")
        glm_doi = "10.5067/GLM/GRID/DATA101"
        # date_start, date_end = "2024-01-01","2024-01-02"
        download_data(glm_doi, glm_input_file_path, date_start, date_end)
