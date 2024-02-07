import sys, os


sys.path.append(f"{os.getcwd()}lmatools_outer/lamtools")

from pull_from_eds.main import download_nalma_or_glm
from workflow_for_NALMA_GLM.main import convert_nalma_glm
from lmatools_outer.examples.test import generate_nc_for_nalma
from const import BASE_PATH

# download_nalma_or_glm("nalma", '2020-03-05','2020-03-06', BASE_PATH)
# generate_nc_for_nalma(BASE_PATH)
convert_nalma_glm(BASE_PATH)
