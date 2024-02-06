import sys

sys.path.append("/home/asubedi/Desktop/work/LD-scripts/automate_nalma_glm/lmatools_outer/lamtools")
print(sys.path)

from pull_from_eds.main import download_nalma_or_glm
from workflow_for_NALMA_GLM.main import convert_nalma_glm
from lmatools_outer.examples.test import generate_nc_for_nalma
from const import BASE_PATH


download_nalma_or_glm("nalma", '2020-01-01','2020-01-02', BASE_PATH)
generate_nc_for_nalma(BASE_PATH)
# convert_nalma_glm(BASE_PATH)