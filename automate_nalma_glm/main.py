from pull_from_eds.main import download_nalma_or_glm
from workflow_for_NALMA_GLM.main import convert_nalma_glm
from lmatools.examples.test import generate_nc_for_nalma
from .const import BASE_PATH

download_nalma_or_glm("nalma", '2020-01-01','2020-01-02', BASE_PATH)
# generate_nc_for_nalma(BASE_PATH)
# convert_nalma_glm(BASE_PATH)