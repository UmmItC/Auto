import os
import time
import json
import requests
import signal

# ANSI color escape codes
class colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    DARK_RED = '\033[31m'
    END = '\033[0m'

# ASCII banner
banner = """
    // | |                              //   ) )              //   ) )   
   //__| |            __  ___  ___     //        ( ) __  ___ //___/ /          // //  
  / ___  |   //   / /  / /   //   ) ) //  ____  / /   / /   / ____ / //   / / // //   
 //    | |  //   / /  / /   //   / / //    / / / /   / /   //       //   / / // //    
//     | | ((___( (  / /   ((___/ / ((____/ / / /   / /   //       ((___( ( // //
"""

creator = "Create by: UmmIt"
version = "v0.1"
interval = 7200

def git_pull(path, url):
    try:
        os.chdir(path)  # Change directory to the repository path
        # Check if the URL is reachable
        response = requests.head(url)
        if response.status_code == 200:
            os.system("git pull origin pages")
        else:
            print(f"{colors.RED}Error: URL '{url}' is not reachable.{colors.END}")
    except Exception as e:
        print(f"{colors.RED}Error occurred while pulling updates from {url} in path {path}: {str(e).split(': ')[-1]}{colors.END} \nPlease ensure the pulling URL is correct.")
        exit()

def main():

    # Signal handler for Ctrl+C
    def signal_handler(sig, frame):
        print(f"\n{colors.YELLOW}Exiting the program...{colors.END}")
        exit(0)

    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Print ASCII banner
    print(colors.DARK_RED + banner + colors.END)

    # Print creator and version in different colors
    print(f"{colors.YELLOW}{creator:<50}{colors.GREEN}{version:>30}{colors.END}\n")

    # Read paths and URLs from JSON file
    try:
        with open("paths_and_urls.json") as file:
            data = json.load(file)
            repositories = data["repositories"]
    except FileNotFoundError:
        print(f"{colors.RED}Error: File 'paths_and_urls.json' not found.{colors.END}")
        return

    while True:
        print("Pulling updates from repositories...")
        for repo in repositories:
            try:
                path = repo["path"]
                url = repo["url"]
                git_pull(path, url)
                print(f"{colors.GREEN}Git pull executed for {url} in path {path}.{colors.END}")
            except KeyError:
                print(f"{colors.RED}Error: Malformed JSON data. 'path' or 'url' key not found in repository.{colors.END}")
            except Exception as e:
                print(f"{colors.RED}Unexpected error: {str(e).split(': ')[-1]}{colors.END}")
        print("Waiting for next pull...")
        time.sleep(interval)

if __name__ == "__main__":
    main()
