
class Wallet:

    def __init__(self, trading_budget = 100, max_amount_per_trade = 25):
        self.trading_budget = trading_budget
        self.max_amount_per_trade = max_amount_per_trade
        self.coins = []
    
    def add_coin_to_wallet(self, coin_name, amount):
        for coin in self.coins:
            if coin_name == coin[0]:
                coin[1] += amount
                return
        self.coins.append((coin_name, amount))
    
    def trading_budget_left(self):
        None

if __name__ == "__main__":
    print("running wallet")