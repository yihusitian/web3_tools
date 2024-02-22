from util.web3util import Web3Util
from uniswap_util import UniswapUtil
from config import CONFIG_OBJ

uniswapWallet = CONFIG_OBJ['uniswapWallet']
uniswapUtil = UniswapUtil(uniswapWallet['address'], uniswapWallet['privateKey'])
uniswapUtil.monitorTokenPrice("0x566e95139e4DE1Bfa505a598EC3A9dA4Cfa879EC", 312, 30)


exit(0)
web3Util = Web3Util()
tokenInfo = web3Util.getTokenInfoByContract("0xB8c77482e45F1F44dE1745F52C74426C631bDD52")
print(tokenInfo)