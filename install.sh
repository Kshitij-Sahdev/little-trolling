#!/bin/bash

# Network Prankster Installation Script - Universal Linux Version
# Updated: 2025-07-11 by Kshitij-Sahdev

echo -e "\e[1;36mNetwork Prankster - Universal Installation Script\e[0m"
echo -e "\e[1;33mDetecting environment and setting up...\e[0m"

# Detect environment
IS_TERMUX=false
if [ -d "/data/data/com.termux" ]; then
    IS_TERMUX=true
    echo -e "\e[1;32mTermux environment detected!\e[0m"
else
    echo -e "\e[1;32mStandard Linux environment detected!\e[0m"
fi

# Detect package manager
PKG_MANAGER=""
if command -v apt >/dev/null 2>&1; then
    PKG_MANAGER="apt"
    echo -e "\e[1;34mDebian/Ubuntu based system detected.\e[0m"
elif command -v pacman >/dev/null 2>&1; then
    PKG_MANAGER="pacman"
    echo -e "\e[1;34mArch Linux based system detected.\e[0m"
elif command -v dnf >/dev/null 2>&1; then
    PKG_MANAGER="dnf"
    echo -e "\e[1;34mFedora/RHEL based system detected.\e[0m"
elif command -v zypper >/dev/null 2>&1; then
    PKG_MANAGER="zypper"
    echo -e "\e[1;34mOpenSUSE based system detected.\e[0m"
elif command -v pkg >/dev/null 2>&1; then
    PKG_MANAGER="pkg"
    echo -e "\e[1;34mTermux package manager detected.\e[0m"
else
    echo -e "\e[1;31mUnable to detect package manager. Please install dependencies manually.\e[0m"
    echo -e "\e[1;33mRequired: python, nmap, net-tools, bluez\e[0m"
    exit 1
fi

# Update package lists
echo -e "\e[1;34mUpdating package lists...\e[0m"
if [ "$PKG_MANAGER" = "apt" ]; then
    sudo apt update -y
elif [ "$PKG_MANAGER" = "pacman" ]; then
    sudo pacman -Sy
elif [ "$PKG_MANAGER" = "dnf" ]; then
    sudo dnf check-update
elif [ "$PKG_MANAGER" = "zypper" ]; then
    sudo zypper refresh
elif [ "$PKG_MANAGER" = "pkg" ]; then
    pkg update -y
fi

# Install required packages
echo -e "\e[1;34mInstalling required packages...\e[0m"
if [ "$PKG_MANAGER" = "apt" ]; then
    sudo apt install -y python3 python3-pip nmap net-tools bluez
elif [ "$PKG_MANAGER" = "pacman" ]; then
    sudo pacman -S --noconfirm python python-pip nmap net-tools bluez bluez-utils
elif [ "$PKG_MANAGER" = "dnf" ]; then
    sudo dnf install -y python3 python3-pip nmap net-tools bluez
elif [ "$PKG_MANAGER" = "zypper" ]; then
    sudo zypper install -y python3 python3-pip nmap net-tools bluez
elif [ "$PKG_MANAGER" = "pkg" ]; then
    pkg install -y python nmap net-tools termux-api root-repo proot tsu bluez
    # Setup termux API
    echo -e "\e[1;34mSetting up Termux API...\e[0m"
    termux-setup-storage
fi

# Install Python requirements
echo -e "\e[1;34mInstalling Python requirements...\e[0m"
if [ "$IS_TERMUX" = true ]; then
    pip install -r requirements.txt
else
    pip3 install -r requirements.txt
fi

# Enable Bluetooth service (for non-Termux environments)
if [ "$IS_TERMUX" = false ]; then
    echo -e "\e[1;34mEnsuring Bluetooth service is enabled...\e[0m"
    if command -v systemctl >/dev/null 2>&1; then
        sudo systemctl enable bluetooth.service
        sudo systemctl start bluetooth.service
        echo -e "\e[1;32mBluetooth service enabled and started!\e[0m"
    else
        echo -e "\e[1;33mCould not enable Bluetooth service automatically.\e[0m"
        echo -e "\e[1;33mYou may need to enable it manually for your system.\e[0m"
    fi
fi

# Create directory for the tool
echo -e "\e[1;34mSetting up the Network Prankster directories...\e[0m"
mkdir -p ~/network-prankster

# Copy script to the directory if not already there
if [ ! -f ~/network-prankster/network_prankster.py ]; then
    cp network_prankster.py ~/network-prankster/
fi
chmod +x ~/network-prankster/network_prankster.py

echo -e "\e[1;32mInstallation complete!\e[0m"
echo -e "\e[1;33mTo run the tool:\e[0m"
echo -e "cd ~/network-prankster"
if [ "$IS_TERMUX" = true ]; then
    echo -e "python network_prankster.py"
else
    echo -e "python3 network_prankster.py"
    echo -e "For full functionality, you might need to run as root:"
    echo -e "sudo python3 network_prankster.py"
fi

# Create a shortcut
echo -e "\e[1;34mCreating a shortcut command...\e[0m"
if [ "$IS_TERMUX" = true ]; then
    echo "alias network-prankster='python ~/network-prankster/network_prankster.py'" >> ~/.bashrc
    echo -e "\e[1;32mShortcut created! You can now type 'network-prankster' to run the tool.\e[0m"
else
    if [ -f ~/.bashrc ]; then
        echo "alias network-prankster='python3 ~/network-prankster/network_prankster.py'" >> ~/.bashrc
        echo -e "\e[1;32mShortcut created in ~/.bashrc! You can now type 'network-prankster' to run the tool.\e[0m"
    elif [ -f ~/.zshrc ]; then
        echo "alias network-prankster='python3 ~/network-prankster/network_prankster.py'" >> ~/.zshrc
        echo -e "\e[1;32mShortcut created in ~/.zshrc! You can now type 'network-prankster' to run the tool.\e[0m"
    else
        echo -e "\e[1;33mCould not create shortcut. No .bashrc or .zshrc found.\e[0m"
    fi
fi

echo -e "\e[1;33mPlease restart your terminal or run 'source ~/.bashrc' to apply changes.\e[0m"
