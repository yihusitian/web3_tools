from web3 import Web3
import mnemonic

w3 = Web3()
mnemo = mnemonic.Mnemonic('english')

class Web3EthWalletTool(object):

    """
        生成多个钱包且返回助记词和私钥
    """
    @classmethod
    def generateWallet(cls, walletNum):
        #生成助记词
        mnemonicPharse = cls.generateMnemonic()
        #生成私钥
        privateKey, accountAddress = cls.getPrivateKeyByMnemonic(mnemonicPharse)
        #生成指定数量的钱包
        wallets = cls.generateWalletByMnemonic(mnemonicPharse, walletNum)
        return {
            "mnemonicPharse": mnemonicPharse,
            "privateKey": privateKey,
            "accountAddress": accountAddress,
            "wallets": wallets
        }

    """
        生成助记词，可以指定强度128～256，默认为128
    """
    @classmethod
    def generateMnemonic(cls, strength=128):
        return mnemo.generate(strength)

    """
        基于助记词生成私钥
    """
    @classmethod
    def getPrivateKeyByMnemonic(cls, mnemonicPharse):
        if not mnemonicPharse:
            raise Exception("助记词不能为空")
        #生成种子
        seed = mnemo.to_seed(mnemonicPharse)
        #基于种子导入账号
        account = w3.eth.account.from_key(Web3.keccak(seed))
        private_key = account.key.hex()
        return private_key, account.address

    @classmethod
    def generateWalletByMnemonic(cls, mnemonicPharse, walletNum, fromIndex=0):
        if not mnemonicPharse or walletNum <= 0:
            raise Exception("助记词不能为空且钱包数量必须大于0")
        w3.eth.account.enable_unaudited_hdwallet_features()
        result = []
        for i in range(fromIndex, fromIndex + walletNum):
            account = w3.eth.account.from_mnemonic(mnemonicPharse, account_path=f"m/44'/60'/0'/0/{i}")
            result.append({
                "address": account.address,
                "private_key": account.key.hex(),
                "index": i
            })
        return result

    @classmethod
    def generateWalletByPrivateKey(cls, privateKey, walletNum, fromIndex=0):
        if not privateKey:
            raise Exception("私钥不能为空")
        w3.eth.account.enable_unaudited_hdwallet_features()
        result = []
        for i in range(fromIndex, fromIndex + walletNum):
            account = w3.eth.account.from_key(privateKey)
            result.append({
                "address": account.address,
                "private_key": account.key.hex()
            })
        return result