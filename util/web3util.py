import json

import requests
from web3 import Web3
import os
from config import PROJECT_PATH, PROVIDER_URL

contract_abi_path = os.path.join(PROJECT_PATH, "contract_abi")
class Web3Util(object):

    def __init__(self):
        self.w3 = self.initWeb3()

    """
     初始化web3对象
    """
    def initWeb3(self):
        try:
            w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))
            print(f"建立连接:{w3.is_connected()}")
            return w3
        except Exception as exection:
            print(f"初始化web3对象异常, e:{exection}")
            raise exection

    """
        获取指定区块信息
    """
    def getBlock(self, blockNumber):
        return self.w3.eth.get_block(blockNumber)

    """
        获取最近的区块信息
    """
    def getLatestBlock(self):
        return self.getBlock('latest')

    """
        直接获取web3对象
    """
    def getWeb3Instance(self):
        return self.w3

    """
        获取指定钱包地址的余额，单位为wei
    """
    def getBalance(self, address, unit="wei"):
        balance = self.w3.eth.get_balance(address)
        return self.w3.from_wei(balance, unit)

    """
        获取指定hash的交易信息
    """
    def getTransaction(self, tx_hash):
        return self.w3.eth.get_transaction(tx_hash)

    """
        获取合约代币的信息
    """
    def getTokenInfoByContract(self, contractAddress):
        # 创建代币合约实例
        contractInstance = self.buildContractInstance(contractAddress)
        # 查询代币的单位（小数位数）
        decimals = contractInstance.functions.decimals().call()
        # 查询代币名称
        tokenName = contractInstance.functions.name().call()
        # 查询代币符号
        symbol = contractInstance.functions.symbol().call()
        # 查询代币总量
        totalSupply = contractInstance.functions.totalSupply().call()
        return {
            "totalSupply": totalSupply,
            "symbol": symbol,
            "tokenName": tokenName,
            "decimals": decimals
        }


    """
        查询代币的小数位数
    """
    def getTokenContractDecimals(self, contractAddress):
        # 创建代币合约实例
        contractInstance = self.buildContractInstance(contractAddress)
        # 查询代币的单位（小数位数）
        decimals = contractInstance.functions.decimals().call()
        return decimals

    """
        构建合约实例对象
    """
    def buildContractInstance(self, contractAddress):
        checkSumContractAddress = Web3.to_checksum_address(contractAddress)
        contractAbi = Web3Util.getContractABI(contractAddress)
        return self.w3.eth.contract(address=checkSumContractAddress, abi=contractAbi)

    @classmethod
    def getContractABI(cls, contractAddress):
        abi_file = os.path.join(contract_abi_path, f"{contractAddress}.json")
        if os.path.isfile(abi_file):
            #如果文件存在，则直接加载文件并返回
            with open(abi_file, "r") as file:
                return json.load(file)
        else:
            return Web3Util.requestAbiAndStore(contractAddress)

    @classmethod
    def requestAbiAndStore(cls, contractAddress):
        url = f"https://api.etherscan.io/api?module=contract&action=getabi&address={contractAddress}"
        response = requests.get(url)
        abi_info = None
        if response.status_code == 200:
            data = json.loads(response.text)
            abi_info = data['result']
        else:
            print("请求失败")
            return
        if abi_info:
            abi_file = os.path.join(contract_abi_path, f"{contractAddress}.json")
            with open(abi_file, "w") as file:
                file.write(abi_info)
        return abi_info