AMOUNT_FROM = 0.08
AMOUNT_TO = 0.086
# Chain list: "zksync", "arbitrum", "optimism", "base"
FROM_CHAIN = "zksync" 
TO_CHAIN = "optimism" 

SHUFFLE_WALLETS = True

TRANSFER_ALL_AMOUNT = False
KEEP_VALUE_FROM = 0.00019 # used only when TRANSFER_ALL_AMOUNT = TRUE
KEEP_VALUE_TO = 0.0003 # used only when TRANSFER_ALL_AMOUNT = TRUE

SLEEP_FROM = 50  # Second
SLEEP_TO = 180  # Second