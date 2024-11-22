import os
import platform
import subprocess
import urllib.request
import zipfile
import sys

def download_git():
    # Define paths and URLs
    git_bin_path = os.path.join(".\\bin\\git\\", "git.exe")
    download_url_win = "https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.1/Git-2.42.0-64-bit.exe"
    download_url_linux = "https://github.com/git/git/archive/refs/tags/v2.42.0.tar.gz"
    download_url_mac = "https://github.com/git/git/archive/refs/tags/v2.42.0.tar.gz"
    
    if os.path.exists(git_bin_path):
        print("Git is already installed.")
        return
    
    system_platform = platform.system().lower()

    if system_platform == "windows":
        print("Git not found, downloading Git for Windows...")
        download_git_windows(download_url_win)
    
    elif system_platform == "linux":
        print("Git not found, downloading Git for Linux...")
        download_git_linux(download_url_linux)
    
    elif system_platform == "darwin":
        print("Git not found, downloading Git for macOS...")
        download_git_mac(download_url_mac)
    
    else:
        print("Unsupported OS detected.")
        sys.exit(1)

def download_git_windows(url):
    # Download and run Git for Windows installer
    try:
        installer_path = ".\\git_installer.exe"
        print("Downloading installer...")
        urllib.request.urlretrieve(url, installer_path)
        print("Installer downloaded.")
        print("Running installer...")
        subprocess.run([installer_path, "/VERYSILENT"], check=True)
        print("Git installation complete.")
    except Exception as e:
        print(f"Error downloading or installing Git: {e}")
        sys.exit(1)

def download_git_linux(url):
    # Placeholder for Git installation on Linux, typically through package managers like apt or yum
    print("Please install Git manually using your package manager.")
    sys.exit(1)

def download_git_mac(url):
    # Placeholder for Git installation on macOS, typically through Homebrew or other methods
    print("Please install Git manually using Homebrew or other package manager.")
    sys.exit(1)

# Run the function to check and install Git if necessary
download_git()
