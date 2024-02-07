import sys, os

path = f"{os.getcwd()}/lmatools_outer/lmatools"
sys.path.append(path)
print(path)

from pull_from_eds.main import download_nalma_or_glm
from workflow_for_NALMA_GLM.main import convert_nalma_glm
from lmatools_outer.examples.test import generate_nc_for_nalma
from const import BASE_PATH


def start(dataset_name, date_start, date_end):
    download_nalma_or_glm(dataset_name, date_start, date_end, BASE_PATH)
    if dataset_name == 'nalma':
        generate_nc_for_nalma(BASE_PATH)
    convert_nalma_glm(BASE_PATH)

#sample nalma test
dataset_name = 'nalma'
date_start, date_end = '2020-03-05','2020-03-06'

#sample glm test
dataset_name = 'glm'
date_start = "2024-01-01 00:00:00"
date_end = "2024-01-01 01:59:59"

#start processing
start(dataset_name, date_start, date_end)