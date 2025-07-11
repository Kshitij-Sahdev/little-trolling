#!/bin/bash

# Network Prankster Installation Script for Termux
echo -e "\e[1;36mNetwork Prankster - Installation Script\e[0m"
echo -e "\e[1;33mSetting up the environment...\e[0m"

# Update packages
echo -e "\e[1;34mUpdating package lists...\e[0m"
pkg update -y

# Install required packages
echo -e "\e[1;34mInstalling required packages...\e[0m"
pkg install -y python nmap net-tools termux-api root-repo proot tsu

# Try to install Bluetooth tools
echo -e "\e[1;34mAttempting to install Bluetooth tools...\e[0m"
pkg install -y bluez

# Setup termux API
echo -e "\e[1;34mSetting up Termux API...\e[0m"
termux-setup-storage

# Create directory for the tool
mkdir -p ~/network-prankster

# Copy script
echo -e "\e[1;34mSetting up the Network Prankster script...\e[0m"
cp network_prankster.py ~/network-prankster/
chmod +x ~/network-prankster/network_prankster.py

echo -e "\e[1;32mInstallation complete!\e[0m"
echo -e "\e[1;33mTo run the tool:\e[0m"
echo -e "cd ~/network-prankster"
echo -e "python network_prankster.py"

# Create a shortcut
echo -e "\e[1;34mCreating a shortcut command...\e[0m"
echo "alias network-prankster='python ~/network-prankster/network_prankster.py'" >> ~/.bashrc
echo -e "\e[1;32mShortcut created! You can now type 'network-prankster' to run the tool.\e[0m"
echo -e "\e[1;33mPlease restart Termux or run 'source ~/.bashrc' to apply changes.\e[0m"
