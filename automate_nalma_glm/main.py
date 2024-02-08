import sys, os

path = f"{os.getcwd()}/lmatools_outer/lmatools"
sys.path.append(path)
print(path)

from pull_from_eds.main import download_nalma_or_glm
from workflow_for_NALMA_GLM.main import convert_nalma_glm
from lmatools_outer.examples.test import generate_nc_for_nalma
from upload_to_bucket.main import upload_directory_contents_to_s3
from const import BASE_PATH
import shutil

bucket_name = 'cog-nalma-glm'

def start(dataset_name, date_start, date_end):
    print(f"{BASE_PATH}data/")
    shutil.rmtree(f"{BASE_PATH}data/")
    download_nalma_or_glm(dataset_name, date_start, date_end, BASE_PATH)
    #local path needed for s3 upload
    local_path = f'{BASE_PATH}data/'
    if dataset_name == 'nalma':
        generate_nc_for_nalma(BASE_PATH)
        local_path += 'nalma_final_output/'
    else:
        local_path += 'glm_final_output/GLM/'

    convert_nalma_glm(BASE_PATH)

    print(">>>>Uploading COG to the bucket....")
    # Upload directory contents to S3
    s3_prefix = dataset_name
    upload_directory_contents_to_s3(local_path, bucket_name, s3_prefix)

#sample nalma test
# dataset_name = 'nalma'
# date_start, date_end = '2020-03-05','2020-03-06'

#sample glm test
dataset_name = 'glm'
date_start = "2024-01-01 00:00:00"
date_end = "2024-01-01 00:01:00"

#start processing
start(dataset_name, date_start, date_end)

