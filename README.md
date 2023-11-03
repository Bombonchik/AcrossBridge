# Across Bridge

## Overview

This application allows you to bridge funds between ZkSync, Arbitrum, Optimism, Base using the Across Bridge. The Across Bridge is a cost-effective way to perform bridge transactions.

## Getting Started

Follow these steps to get started:

1. **Set Up Your Private Keys**

   - Add your private keys to `accounts.txt` in the `data` directory, with each key on a separate line. These private keys are essential for signing transactions and interacting with the bridge.

2. **Configure the Application**

   - Open the `settings.py` file in the project directory.
   - Update the configuration settings based on your needs. 
   - You can input your own RPC in `data/rpc.json` 

## Running the Application

Once you have set up your private keys and configured the application, you can run it to start bridging funds. Make sure you have the necessary dependencies and libraries installed before running the application.

```bash
# Run the bridge application
pip install -r requirements 
python main.py