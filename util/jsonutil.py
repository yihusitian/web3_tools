import json
import os

"""
    加载json文件为字典对象
"""
def loadJsonToDic(json_file):
    if not os.path.isfile(json_file):
        raise Exception(f"{json_file}不存在")
    try:
        with open(json_file, "r") as jsonFile:
            return json.load(jsonFile)
    except Exception as e:
        raise Exception(f"加载文件{json_file}异常")
        print(f"加载文件{json_file}异常, e:{e}")