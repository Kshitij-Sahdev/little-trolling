#!/usr/bin/env python3
"""
Network & Bluetooth Scanner + Harmless Pranking Tool
For educational purposes and demonstrating network security skills

Run in Termux on Android (Debian)
Requires: Termux with Debian installed, root access for some features
"""

import os
import sys
import time
import json
import random
import subprocess
import threading
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Set

# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

class NetworkPrankster:
    def __init__(self):
        """Initialize the Network Prankster tool."""
        self.version = "1.0.0"
        self.bluetooth_devices = {}
        self.wifi_devices = {}
        self.scan_history = []
        self.is_scanning = False
        self.last_scan_time = None
        self.prank_modes = {
            "1": "notification_bomb", 
            "2": "bt_rename_spoof",
            "3": "wifi_deauth_prank",
            "4": "bt_sound_play"
        }
        
        # Check for required tools
        self.check_requirements()

    def print_banner(self):
        """Print the tool's banner."""
        banner = f"""
{Colors.CYAN}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║  {Colors.RED}███╗   ██╗███████╗████████╗██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗{Colors.CYAN}    ║
║  {Colors.RED}████╗  ██║██╔════╝╚══██╔══╝██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝{Colors.CYAN}    ║
║  {Colors.RED}██╔██╗ ██║█████╗     ██║   ██║ █╗ ██║██║   ██║██████╔╝█████╔╝ {Colors.CYAN}    ║
║  {Colors.RED}██║╚██╗██║██╔══╝     ██║   ██║███╗██║██║   ██║██╔══██╗██╔═██╗ {Colors.CYAN}    ║
║  {Colors.RED}██║ ╚████║███████╗   ██║   ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗{Colors.CYAN}    ║
║  {Colors.RED}╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝{Colors.CYAN}    ║
║                                                                   ║
║  {Colors.PURPLE}██████╗ ██████╗  █████╗ ███╗   ██╗██╗  ██╗███████╗████████╗███████╗██████╗ {Colors.CYAN} ║
║  {Colors.PURPLE}██╔══██╗██╔══██╗██╔══██╗████╗  ██║██║ ██╔╝██╔════╝╚══██╔══╝██╔════╝██╔══██╗{Colors.CYAN} ║
║  {Colors.PURPLE}██████╔╝██████╔╝███████║██╔██╗ ██║█████╔╝ ███████╗   ██║   █████╗  ██████╔╝{Colors.CYAN} ║
║  {Colors.PURPLE}██╔═══╝ ██╔══██╗██╔══██║██║╚██╗██║██╔═██╗ ╚════██║   ██║   ██╔══╝  ██╔══██╗{Colors.CYAN} ║
║  {Colors.PURPLE}██║     ██║  ██║██║  ██║██║ ╚████║██║  ██╗███████║   ██║   ███████╗██║  ██║{Colors.CYAN} ║
║  {Colors.PURPLE}╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝{Colors.CYAN} ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.YELLOW}[*] Termux Network Prankster v{self.version} - by Kshitij-Sahdev
[*] For educational purposes only. Use responsibly.
[*] Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}
        """
        print(banner)

    def check_requirements(self):
        """Check if all required tools are installed."""
        required_tools = {
            "hcitool": "Bluetooth utilities (apt install bluez)",
            "bluetoothctl": "Bluetooth control (apt install bluez)",
            "l2ping": "Bluetooth ping utility (apt install bluez)",
            "bluetoothd": "Bluetooth daemon (apt install bluez)",
            "ip": "Network utilities (pre-installed)",
            "arp": "ARP utilities (apt install net-tools)",
            "nmap": "Network mapper (apt install nmap)",
            "termux-notification": "Termux API (pkg install termux-api)"
        }
        
        missing_tools = []
        
        for tool, description in required_tools.items():
            try:
                subprocess.run(["which", tool], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            except subprocess.CalledProcessError:
                missing_tools.append(f"{tool} - {description}")
        
        if missing_tools:
            print(f"{Colors.RED}[!] Missing required tools:{Colors.END}")
            for tool in missing_tools:
                print(f"{Colors.RED}    - {tool}{Colors.END}")
            print(f"\n{Colors.YELLOW}[*] Install missing tools with:{Colors.END}")
            print(f"{Colors.YELLOW}    pkg install root-repo{Colors.END}")
            print(f"{Colors.YELLOW}    pkg install termux-api nmap net-tools bluez{Colors.END}")
            print(f"{Colors.YELLOW}    termux-setup-storage{Colors.END}")
            print(f"{Colors.RED}[!] Some features might not work without all required tools.{Colors.END}\n")

    def scan_bluetooth_devices(self) -> Dict:
        """Scan for nearby Bluetooth devices."""
        print(f"{Colors.BLUE}[*] Scanning for Bluetooth devices...{Colors.END}")
        devices = {}
        
        try:
            # Try using hcitool to scan for devices
            output = subprocess.check_output(["hcitool", "scan"], universal_newlines=True, stderr=subprocess.DEVNULL)
            lines = output.strip().split('\n')[1:]  # Skip the "Scanning ..." line
            
            for line in lines:
                if '\t' in line:
                    mac, name = line.strip().split('\t', 1)
                    devices[mac] = {
                        "name": name,
                        "type": self.get_device_type(name),
                        "first_seen": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "last_seen": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "signal_strength": "N/A",
                        "pranked": False
                    }
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                # Alternative: try bluetoothctl
                process = subprocess.Popen(["bluetoothctl"], stdin=subprocess.PIPE, 
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                         text=True)
                
                commands = "scan on\n"
                time.sleep(5)  # Scan for 5 seconds
                commands += "devices\n"
                commands += "scan off\n"
                commands += "quit\n"
                
                output, _ = process.communicate(commands)
                
                # Parse the output for devices
                device_lines = [l for l in output.split('\n') if "Device" in l]
                for line in device_lines:
                    parts = line.strip().split(' ', 2)
                    if len(parts) >= 3:
                        mac = parts[1]
                        name = parts[2] if len(parts) > 2 else "Unknown"
                        devices[mac] = {
                            "name": name,
                            "type": self.get_device_type(name),
                            "first_seen": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            "last_seen": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            "signal_strength": "N/A",
                            "pranked": False
                        }
            except:
                print(f"{Colors.RED}[!] Failed to scan Bluetooth devices. Make sure Bluetooth is enabled.{Colors.END}")
        
        # Update the existing devices dictionary
        for mac, device_info in devices.items():
            if mac in self.bluetooth_devices:
                device_info["first_seen"] = self.bluetooth_devices[mac]["first_seen"]
                device_info["pranked"] = self.bluetooth_devices[mac]["pranked"]
            self.bluetooth_devices[mac] = device_info
            
        print(f"{Colors.GREEN}[+] Found {len(devices)} Bluetooth devices{Colors.END}")
        return self.bluetooth_devices

    def scan_wifi_devices(self) -> Dict:
        """Scan for devices on the WiFi network."""
        print(f"{Colors.BLUE}[*] Scanning for WiFi devices...{Colors.END}")
        devices = {}
        
        try:
            # Get our IP address and network
            ip_output = subprocess.check_output(["ip", "route"], universal_newlines=True)
            network = None
            for line in ip_output.split('\n'):
                if "default via" in line:
                    parts = line.split()
                    gateway = parts[2]
                    break
            
            if not gateway:
                print(f"{Colors.RED}[!] Could not determine network gateway.{Colors.END}")
                return devices
                
            # Run a quick nmap scan on the local network
            print(f"{Colors.BLUE}[*] Running nmap scan (this might take a minute)...{Colors.END}")
            nmap_output = subprocess.check_output(
                ["nmap", "-sn", gateway + "/24"], 
                universal_newlines=True, 
                stderr=subprocess.DEVNULL
            )
            
            # Parse nmap output
            ip_pattern = re.compile(r'Nmap scan report for (?:([^\s]+) )?(\d+\.\d+\.\d+\.\d+)')
            mac_pattern = re.compile(r'MAC Address: ([0-9A-F:]{17}) \(([^)]+)\)')
            
            current_ip = None
            
            for line in nmap_output.split('\n'):
                ip_match = ip_pattern.search(line)
                if ip_match:
                    hostname = ip_match.group(1) or "Unknown"
                    current_ip = ip_match.group(2)
                    devices[current_ip] = {
                        "ip": current_ip,
                        "hostname": hostname,
                        "mac": "Unknown",
                        "vendor": "Unknown",
                        "first_seen": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "last_seen": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "pranked": False
                    }
                
                mac_match = mac_pattern.search(line)
                if mac_match and current_ip:
                    devices[current_ip]["mac"] = mac_match.group(1)
                    devices[current_ip]["vendor"] = mac_match.group(2)
        
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"{Colors.RED}[!] Error scanning WiFi network: {str(e)}{Colors.END}")
            
            # Try alternative approach using arp
            try:
                arp_output = subprocess.check_output(["arp", "-a"], universal_newlines=True)
                for line in arp_output.split('\n'):
                    if '(' in line and ')' in line:
                        parts = line.split()
                        if len(parts) >= 4:
                            hostname = parts[0]
                            ip = parts[1].strip('()')
                            mac = parts[3]
                            devices[ip] = {
                                "ip": ip,
                                "hostname": hostname,
                                "mac": mac,
                                "vendor": "Unknown",
                                "first_seen": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                "last_seen": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                "pranked": False
                            }
            except:
                print(f"{Colors.RED}[!] Failed to scan WiFi devices using alternative method.{Colors.END}")
        
        # Update the existing devices dictionary
        for ip, device_info in devices.items():
            if ip in self.wifi_devices:
                device_info["first_seen"] = self.wifi_devices[ip]["first_seen"]
                device_info["pranked"] = self.wifi_devices[ip]["pranked"]
            self.wifi_devices[ip] = device_info
            
        print(f"{Colors.GREEN}[+] Found {len(devices)} WiFi devices{Colors.END}")
        return self.wifi_devices

    def get_device_type(self, name: str) -> str:
        """Determine device type based on name."""
        name = name.lower()
        
        if not name or name == "unknown":
            return "Unknown"
        
        if any(keyword in name for keyword in ["iphone", "ipad", "macbook", "mac", "apple"]):
            return "Apple"
        elif any(keyword in name for keyword in ["samsung", "galaxy", "sm-"]):
            return "Samsung"
        elif any(keyword in name for keyword in ["mi", "redmi", "xiaomi", "poco"]):
            return "Xiaomi"
        elif any(keyword in name for keyword in ["oneplus", "nord"]):
            return "OnePlus"
        elif any(keyword in name for keyword in ["speaker", "audio", "headphone", "buds"]):
            return "Audio Device"
        elif any(keyword in name for keyword in ["tv", "television"]):
            return "TV"
        elif any(keyword in name for keyword in ["car", "auto"]):
            return "Car"
        else:
            return "Generic Device"

    def send_notification_prank(self, device_name: str) -> bool:
        """Send a harmless fake notification to user's phone."""
        try:
            fake_notifications = [
                {"title": "Low Battery Warning", "content": "Battery at 3%. Connect charger immediately."},
                {"title": "Software Update", "content": f"New system update available for {device_name}"},
                {"title": "Wi-Fi Security", "content": "Open network detected. Your device may be vulnerable."},
                {"title": "Device Manager", "content": "Unknown device accessing your account from new location"},
                {"title": "Storage Alert", "content": "Storage space critically low. Delete files to continue."},
                {"title": "System Performance", "content": "Multiple apps draining battery in background"}
            ]
            
            notification = random.choice(fake_notifications)
            
            subprocess.run([
                "termux-notification",
                "--title", notification["title"],
                "--content", notification["content"],
                "--vibrate", "500,200,500",
                "--led-color", "FF0000",
                "--priority", "high"
            ])
            
            print(f"{Colors.GREEN}[+] Sent prank notification: {notification['title']}{Colors.END}")
            return True
        except Exception as e:
            print(f"{Colors.RED}[!] Failed to send notification: {str(e)}{Colors.END}")
            return False

    def bt_rename_spoof(self, device_mac: str) -> bool:
        """Temporarily spoof your device name to confuse nearby Bluetooth users."""
        try:
            funny_names = [
                "FBI Surveillance Van",
                "COVID-19 Tracker",
                "Hack_Detector_v2",
                "Free WiFi Hotspot",
                "Connect for Prize",
                "NASA Deep Space Network",
                "Your Phone Backup",
                "Unknown Device (0)",
                "Network Security Scanner",
                "Totally Not A Virus"
            ]
            
            # Save original name
            original_name = subprocess.check_output(
                ["bluetoothctl", "show"], universal_newlines=True
            )
            match = re.search(r'Name: (.+)', original_name)
            original_name = match.group(1) if match else "Android"
            
            # Set new name
            new_name = random.choice(funny_names)
            subprocess.run(["bluetoothctl", "system-alias", new_name])
            
            print(f"{Colors.GREEN}[+] Spoofed Bluetooth name to '{new_name}'{Colors.END}")
            print(f"{Colors.YELLOW}[*] Waiting 30 seconds before reverting...{Colors.END}")
            
            # Wait a bit and then revert
            time.sleep(30)
            subprocess.run(["bluetoothctl", "system-alias", original_name])
            print(f"{Colors.GREEN}[+] Reverted Bluetooth name to original{Colors.END}")
            
            return True
        except Exception as e:
            print(f"{Colors.RED}[!] Failed to spoof Bluetooth name: {str(e)}{Colors.END}")
            return False

    def bt_sound_play(self, device_mac: str) -> bool:
        """Play a sound on the target Bluetooth device if it's a speaker/headphone."""
        device = self.bluetooth_devices.get(device_mac)
        if not device:
            print(f"{Colors.RED}[!] Device not found{Colors.END}")
            return False
            
        if "Audio" not in device["type"] and not self.confirm_action("This doesn't appear to be an audio device. Try anyway?"):
            return False
            
        try:
            print(f"{Colors.YELLOW}[*] Attempting to connect to Bluetooth device...{Colors.END}")
            subprocess.run(["bluetoothctl", "connect", device_mac], timeout=10)
            
            # If we reach here, we might be connected, try to play a sound
            print(f"{Colors.YELLOW}[*] Connected! Attempting to play sound...{Colors.END}")
            
            # Use termux-media-player to play a sound
            sound_file = "/data/data/com.termux/files/usr/share/sounds/freedesktop/stereo/message.oga"
            if not os.path.exists(sound_file):
                # Create a simple sound file if it doesn't exist
                subprocess.run(["termux-tts-speak", "Hello there! Just a friendly sound test."])
            else:
                subprocess.run(["termux-media-player", "play", sound_file])
                
            time.sleep(3)  # Let the sound play
            
            # Disconnect
            subprocess.run(["bluetoothctl", "disconnect", device_mac])
            print(f"{Colors.GREEN}[+] Sound played and disconnected{Colors.END}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}[!] Failed to play sound: {str(e)}{Colors.END}")
            return False

    def wifi_deauth_prank(self, target_ip: str) -> bool:
        """
        Pretend to deauthenticate a device (just notification).
        NOTE: This doesn't actually deauth - just simulates for educational purposes
        """
        device = self.wifi_devices.get(target_ip)
        if not device:
            print(f"{Colors.RED}[!] Device not found{Colors.END}")
            return False
            
        try:
            print(f"{Colors.YELLOW}[*] Simulating deauthentication of {device['hostname']} ({target_ip})...{Colors.END}")
            
            # This just pretends to run a deauth - IT DOESN'T ACTUALLY DO IT
            for i in range(5):
                print(f"{Colors.YELLOW}[*] Sending simulated deauth packet {i+1}/5...{Colors.END}")
                time.sleep(1)
                
            # Send a notification about what just happened
            subprocess.run([
                "termux-notification",
                "--title", "Network Prank Simulation",
                "--content", f"Simulated deauth on {device['hostname']}. In real pentest, device would disconnect briefly.",
            ])
            
            print(f"{Colors.GREEN}[+] Deauth simulation complete!{Colors.END}")
            print(f"{Colors.GREEN}[+] (Note: No actual deauth occurred, this was just educational){Colors.END}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}[!] Failed to simulate deauth: {str(e)}{Colors.END}")
            return False

    def execute_prank(self, device_type: str, device_id: str, prank_type: str) -> bool:
        """Execute the selected prank on the target device."""
        if prank_type == "notification_bomb":
            return self.send_notification_prank("Your Device")
        elif prank_type == "bt_rename_spoof":
            return self.bt_rename_spoof(device_id)
        elif prank_type == "wifi_deauth_prank":
            return self.wifi_deauth_prank(device_id)
        elif prank_type == "bt_sound_play":
            return self.bt_sound_play(device_id)
        else:
            print(f"{Colors.RED}[!] Unknown prank type: {prank_type}{Colors.END}")
            return False

    def confirm_action(self, message: str) -> bool:
        """Ask for user confirmation before proceeding with action."""
        response = input(f"{Colors.YELLOW}[?] {message} (y/n): {Colors.END}").lower()
        return response in ('y', 'yes')

    def display_bluetooth_devices(self):
        """Display all discovered Bluetooth devices."""
        if not self.bluetooth_devices:
            print(f"{Colors.YELLOW}[*] No Bluetooth devices found. Run a scan first.{Colors.END}")
            return
            
        print(f"\n{Colors.BLUE}{Colors.BOLD}=== BLUETOOTH DEVICES ==={Colors.END}")
        print(f"{Colors.CYAN}{'MAC Address':<18} {'Name':<30} {'Type':<15} {'First Seen':<20} {'Pranked'}{Colors.END}")
        print("-" * 90)
        
        for mac, device in self.bluetooth_devices.items():
            pranked_status = f"{Colors.GREEN}Yes{Colors.END}" if device['pranked'] else f"{Colors.RED}No{Colors.END}"
            print(f"{mac:<18} {device['name']:<30} {device['type']:<15} {device['first_seen']:<20} {pranked_status}")
    
    def display_wifi_devices(self):
        """Display all discovered WiFi devices."""
        if not self.wifi_devices:
            print(f"{Colors.YELLOW}[*] No WiFi devices found. Run a scan first.{Colors.END}")
            return
            
        print(f"\n{Colors.BLUE}{Colors.BOLD}=== WIFI DEVICES ==={Colors.END}")
        print(f"{Colors.CYAN}{'IP Address':<15} {'Hostname':<25} {'MAC Address':<18} {'Vendor':<20} {'Pranked'}{Colors.END}")
        print("-" * 90)
        
        for ip, device in self.wifi_devices.items():
            pranked_status = f"{Colors.GREEN}Yes{Colors.END}" if device['pranked'] else f"{Colors.RED}No{Colors.END}"
            print(f"{ip:<15} {device['hostname'][:25]:<25} {device['mac']:<18} {device['vendor'][:20]:<20} {pranked_status}")

    def show_prank_menu(self):
        """Display the available pranks menu."""
        print(f"\n{Colors.PURPLE}{Colors.BOLD}=== AVAILABLE PRANKS ==={Colors.END}")
        print(f"{Colors.YELLOW}1. Notification Bomb - Send fake system notifications{Colors.END}")
        print(f"{Colors.YELLOW}2. Bluetooth Name Spoof - Temporarily change your device name{Colors.END}")
        print(f"{Colors.YELLOW}3. WiFi Deauth Prank - Simulate disconnection (no actual deauth){Colors.END}")
        print(f"{Colors.YELLOW}4. Bluetooth Speaker Sound - Play sound on connected speaker{Colors.END}")
        print(f"{Colors.YELLOW}0. Back to main menu{Colors.END}")
        
        choice = input(f"{Colors.BLUE}[?] Select a prank (0-4): {Colors.END}")
        
        if choice == "0":
            return None
        elif choice in self.prank_modes:
            return self.prank_modes[choice]
        else:
            print(f"{Colors.RED}[!] Invalid choice{Colors.END}")
            return None

    def select_target_device(self, device_type: str):
        """Let the user select a target device."""
        if device_type == "bluetooth":
            self.display_bluetooth_devices()
            if not self.bluetooth_devices:
                return None
                
            mac = input(f"{Colors.BLUE}[?] Enter MAC address of target device (or 'back'): {Colors.END}")
            if mac.lower() == 'back':
                return None
            elif mac in self.bluetooth_devices:
                return mac
            else:
                print(f"{Colors.RED}[!] Invalid MAC address{Colors.END}")
                return None
        else:  # WiFi
            self.display_wifi_devices()
            if not self.wifi_devices:
                return None
                
            ip = input(f"{Colors.BLUE}[?] Enter IP address of target device (or 'back'): {Colors.END}")
            if ip.lower() == 'back':
                return None
            elif ip in self.wifi_devices:
                return ip
            else:
                print(f"{Colors.RED}[!] Invalid IP address{Colors.END}")
                return None

    def run_scan(self):
        """Run a full network scan."""
        if self.is_scanning:
            print(f"{Colors.YELLOW}[*] Scan already in progress...{Colors.END}")
            return
            
        self.is_scanning = True
        print(f"{Colors.BLUE}[*] Starting full network scan...{Colors.END}")
        
        # Scan for Bluetooth devices
        bt_devices = self.scan_bluetooth_devices()
        
        # Scan for WiFi devices
        wifi_devices = self.scan_wifi_devices()
        
        self.is_scanning = False
        self.last_scan_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Record scan in history
        self.scan_history.append({
            "timestamp": self.last_scan_time,
            "bt_devices_count": len(bt_devices),
            "wifi_devices_count": len(wifi_devices)
        })
        
        print(f"{Colors.GREEN}[+] Scan completed at {self.last_scan_time}{Colors.END}")
        print(f"{Colors.GREEN}[+] Found {len(bt_devices)} Bluetooth devices and {len(wifi_devices)} WiFi devices{Colors.END}")

    def save_results(self):
        """Save scan results to a file."""
        if not self.bluetooth_devices and not self.wifi_devices:
            print(f"{Colors.YELLOW}[*] No scan results to save. Run a scan first.{Colors.END}")
            return
            
        filename = f"network_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        data = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "bluetooth_devices": self.bluetooth_devices,
            "wifi_devices": self.wifi_devices,
            "scan_history": self.scan_history
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"{Colors.GREEN}[+] Results saved to {filename}{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}[!] Failed to save results: {str(e)}{Colors.END}")

    def show_help(self):
        """Display help information."""
        print(f"\n{Colors.BLUE}{Colors.BOLD}=== HELP MENU ==={Colors.END}")
        print(f"{Colors.CYAN}This tool lets you scan for nearby devices and perform harmless pranks.{Colors.END}")
        print(f"\n{Colors.YELLOW}Available commands:{Colors.END}")
        print(f"  {Colors.GREEN}scan{Colors.END} - Run a full network scan for Bluetooth and WiFi devices")
        print(f"  {Colors.GREEN}bluetooth{Colors.END} - Show discovered Bluetooth devices")
        print(f"  {Colors.GREEN}wifi{Colors.END} - Show discovered WiFi devices")
        print(f"  {Colors.GREEN}prank{Colors.END} - Select a prank to perform")
        print(f"  {Colors.GREEN}save{Colors.END} - Save scan results to a file")
        print(f"  {Colors.GREEN}help{Colors.END} - Show this help menu")
        print(f"  {Colors.GREEN}quit{Colors.END} - Exit the program")
        print(f"\n{Colors.YELLOW}Note: Some features require root access and appropriate permissions.{Colors.END}")
        print(f"{Colors.YELLOW}This tool is for educational purposes only. Use responsibly.{Colors.END}")

    def main_menu(self):
        """Display the main menu and handle user input."""
        self.print_banner()
        self.check_requirements()
        
        while True:
            print(f"\n{Colors.BLUE}{Colors.BOLD}=== MAIN MENU ==={Colors.END}")
            print(f"{Colors.YELLOW}1. Run full network scan{Colors.END}")
            print(f"{Colors.YELLOW}2. Show Bluetooth devices{Colors.END}")
            print(f"{Colors.YELLOW}3. Show WiFi devices{Colors.END}")
            print(f"{Colors.YELLOW}4. Select a prank{Colors.END}")
            print(f"{Colors.YELLOW}5. Save results{Colors.END}")
            print(f"{Colors.YELLOW}6. Help{Colors.END}")
            print(f"{Colors.YELLOW}0. Quit{Colors.END}")
            
            choice = input(f"\n{Colors.BLUE}[?] Enter your choice (0-6): {Colors.END}")
            
            if choice == "1":
                self.run_scan()
            elif choice == "2":
                self.display_bluetooth_devices()
            elif choice == "3":
                self.display_wifi_devices()
            elif choice == "4":
                prank_type = self.show_prank_menu()
                if prank_type:
                    if prank_type in ["bt_rename_spoof", "bt_sound_play"]:
                        device_type = "bluetooth"
                    else:
                        device_type = "wifi" if prank_type == "wifi_deauth_prank" else None
                    
                    if device_type:
                        device_id = self.select_target_device(device_type)
                        if device_id and self.confirm_action(f"Perform {prank_type} on selected device?"):
                            success = self.execute_prank(device_type, device_id, prank_type)
                            if success and device_type == "bluetooth":
                                self.bluetooth_devices[device_id]["pranked"] = True
                            elif success and device_type == "wifi":
                                self.wifi_devices[device_id]["pranked"] = True
                    else:
                        # For notification bomb, no target device needed
                        if self.confirm_action(f"Perform {prank_type}?"):
                            self.execute_prank(None, None, prank_type)
            elif choice == "5":
                self.save_results()
            elif choice == "6":
                self.show_help()
            elif choice == "0":
                print(f"{Colors.GREEN}[+] Exiting. Thanks for using Network Prankster!{Colors.END}")
                sys.exit(0)
            else:
                print(f"{Colors.RED}[!] Invalid choice{Colors.END}")

if __name__ == "__main__":
    try:
        prankster = NetworkPrankster()
        prankster.main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Program interrupted by user. Exiting...{Colors.END}")
        sys.exit(0)
