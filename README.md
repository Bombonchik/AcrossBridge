# AcrossBridge

## Overview

This application allows you to bridge funds from zkSync using the Across Bridge. The Across Bridge is a cost-effective way to perform bridge transactions, especially when dealing with large transaction volumes, as compared to the Bungee Gas Refuel.

## Getting Started

Follow these steps to get started with the Funds Bridge Application:

1. **Set Up Your Private Keys**

   - Create a file named `accounts.txt` in the `data` directory.
   - Add your private keys to this file, with each key on a separate line. These private keys are essential for signing transactions and interacting with the bridge.

2. **Configure the Application**

   - Open the `settings.py` file in the project directory.
   - Update the configuration settings based on your needs. Please note that, as of now, only the zkSync -> Arbitrum bridge has been tested.
   - You can input your own RPC in `data/rpc.json` 

## Running the Application

Once you have set up your private keys and configured the application, you can run it to start bridging funds from zkSync to Arbitrum or other supported bridges. Make sure you have the necessary dependencies and libraries installed before running the application.

```bash
# Run the bridge application
pip install -r requirements 
python main.py
```
