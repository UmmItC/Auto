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
version = "v0.2"
interval = 30

def git_pull(path):
    try:
        os.chdir(path)  # Change directory to the repository path
        os.system("git pull origin main")  # Assuming the default branch is 'main'
    except Exception as e:
        print(f"{colors.RED}Error occurred while pulling updates in path {path}: {str(e)}{colors.END}")

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

    # Dictionary to store last update times
    last_update_times = {}

    while True:
        print("Checking for repository updates...")
        for repo in repositories:
            try:
                username = repo["username"]
                repository = repo["repository"]
                url = f"https://codeberg.org/api/v1/repos/{username}/{repository}"
                
                # Fetch repository data
                response = requests.get(url)
                if response.status_code == 200:
                    repo_data = response.json()
                    last_update_time = repo_data["updated_at"]
                    if repository in last_update_times:
                        if last_update_times[repository] != last_update_time:
                            # Repository has been updated, pull changes
                            path = repo["path"]
                            git_pull(path)
                            last_update_times[repository] = last_update_time
                            print(f"{colors.GREEN}Updated repository: {username}/{repository}.{colors.END}")
                    else:
                        # First time checking, store update time
                        last_update_times[repository] = last_update_time
            except Exception as e:
                print(f"{colors.RED}Error occurred while checking repository {username}/{repository}: {str(e)}{colors.END}")

        print("Waiting for next check...")
        time.sleep(interval)

if __name__ == "__main__":
    main()
