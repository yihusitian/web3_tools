import time

from config import PROVIDER_URL
from uniswap import Uniswap
from util.web3util import Web3Util
from web3 import Web3
from alarm.emai_util import sendEmailMessage

web3UtilInstance = Web3Util()
USD_CONTRACT_ADDRESS = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
USD_CONTRACT_CHECKSUM_ADDRESS = Web3.to_checksum_address(USD_CONTRACT_ADDRESS)
USD_CONTRACT_DECIMALS = web3UtilInstance.getTokenContractDecimals(USD_CONTRACT_ADDRESS)
class UniswapUtil(object):
    def __init__(self, walletAddress, walletPrivateKey):
        self.uniswapInstance = Uniswap(address=walletAddress, private_key=walletPrivateKey, version=2, provider=PROVIDER_URL)

    """
        获取Uniswap实例
    """
    def getUniswapInstance(self):
        return self.uniswapInstance

    """
        监控代币的价格
        :param contractAddress: 代币合约的地址
        :param targetPrice: 要监控的目标价格，usd单位
        :param interval: 间隔时间，默认为15秒
    """
    def monitorTokenPrice(self, contractAddress, targetPrice, interval=15):
        while True:
            tokenInfo = web3UtilInstance.getTokenInfoByContract(contractAddress)
            tokenSymbol = tokenInfo['symbol']
            price = self.uniswapInstance.get_price_input(token0=Web3.to_checksum_address(contractAddress), token1=USD_CONTRACT_CHECKSUM_ADDRESS, qty=10 ** tokenInfo['decimals'])
            usdPrice = price / (10 ** USD_CONTRACT_DECIMALS)
            f_usdprice = '{:.20f}'.format(usdPrice)
            print(f"当前价格{f_usdprice} usd")
            if (usdPrice >= targetPrice):
                print(f"当前价格{usdPrice:.8f} usd")
                sendEmailMessage("价格报警通知", f"代币{tokenSymbol}目标价格{targetPrice}已达成，当前价格为{f_usdprice}")
                break
            time.sleep(interval)

    """
        执行买卖交易，即代币兑换
    """
    def makeTrade(self, sellTokenContract, buyTokenContract, sellTokenAmount):
        sellTokenInfo = web3UtilInstance.getTokenInfoByContract(sellTokenContract)
        buyTokenInfo = web3UtilInstance.getTokenInfoByContract(buyTokenContract)
        sellTokenDecimals = sellTokenInfo['decimal']
        walletTokenAmount = self.getTokenAmount(sellTokenContract, sellTokenDecimals)
        sellTokenSymbol = sellTokenInfo['symbol']
        buyTokenSymbol = buyTokenInfo['symbol']
        sellCheckSumAddress = Web3.to_checksum_address(sellTokenContract)
        buyCheckSumAddress = Web3.to_checksum_address(buyTokenContract)
        if walletTokenAmount < sellTokenAmount:
            print(f"钱包剩余代币{sellTokenSymbol}数量{walletTokenAmount}小于卖出数量{sellTokenAmount}不可操作")
            return
        amount_out = int(sellTokenAmount * (10 ** sellTokenInfo['decimal']))
        self.uniswapInstance.make_trade(
            sellCheckSumAddress,  # 换出的币
            buyCheckSumAddress,  # 换入的币
            amount_out,  # 换出币的数量
            recipient=None,
            fee=None,
            slippage=None,
            fee_on_transfer=False  # v3不支持fee_on_transfer
        )
        print(f"购买代币{buyTokenSymbol}成功")

    """
        获取代币的数量
    """
    def getTokenAmount(self, tokenContract, decimals):
        amount_out = self.uniswapInstance.get_token_balance(tokenContract)
        v_amount_ount = amount_out / (10 ** decimals)
        return v_amount_ount
