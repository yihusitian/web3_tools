import json

from web3 import Web3

# 连接到 Binance Smart Chain 节点
bsc_url = "https://bsc-dataseed.binance.org/"  # Binance Smart Chain 的节点URL
w3 = Web3(Web3.HTTPProvider(bsc_url))

# 代币合约地址（PancakeSwap 上的代币）
token_contract_address = Web3.to_checksum_address("0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82")  # 示例代币地址（Binance Coin BNB）

# PancakeSwap Router 合约地址
pancakeswap_router_address = Web3.to_checksum_address("0x05fF2B0DB69458A0750badebc4f9e13aDd608C7F")  # PancakeSwap Router 合约地址

# 代币的精度（通常是 18，以太坊标准）
token_decimals = 18

pancakeswap_router_abi_json = """
[
  {
    "constant": false,
    "inputs": [
      {
        "name": "amountIn",
        "type": "uint256"
      },
      {
        "name": "path",
        "type": "address[]"
      }
    ],
    "name": "getAmountsOut",
    "outputs": [
      {
        "name": "amounts",
        "type": "uint256[]"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
"""
pancakeswap_router_abi = json.loads(pancakeswap_router_abi_json)


# 查询代币价格的函数
def get_token_price():
    # 获取 PancakeSwap Router 合约
    pancakeswap_router = w3.eth.contract(address=pancakeswap_router_address, abi=pancakeswap_router_abi)

    # 查询代币价格（以 Wei 为单位）
    price_in_wei = pancakeswap_router.functions.getAmountsOut(
        10 ** token_decimals,  # 输入数量，这里为 1 个代币
        [token_contract_address, Web3.to_checksum_address("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")]  # 0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c 是 BNB 地址
    ).call()[-1]

    # 转换价格为 BNB 单位
    price_in_bnb = w3.from_wei(price_in_wei, "ether")

    return price_in_bnb

if __name__ == "__main__":
    # 查询代币价格并打印
    token_price = get_token_price()
    print(f"Token Price in BNB: {token_price}")
