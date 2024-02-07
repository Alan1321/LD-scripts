import os

path = os.getcwd()
split = path.split('/')
BASE_PATH = "/".join(split[:-4]) + '/'

print(BASE_PATH)