import os
from util.jsonutil import loadJsonToDic

#当前项目目录
PROJECT_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
CONFIG_PATH = os.path.join(PROJECT_PATH, "data/config.json")
CONFIG_OBJ = loadJsonToDic(CONFIG_PATH)
PROVIDER_URL = f"https://mainnet.infura.io/v3/{CONFIG_OBJ['infuraApiKey']}"