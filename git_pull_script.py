import os
import time
import json
import requests
import signal
from requests.exceptions import HTTPError, RequestException

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

# Read version and coder from file
def read_version_and_coder():
    version = None
    coder = None
    try:
        with open("version", "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("version"):
                    version = line.split("=")[1].strip()
                elif line.startswith("coder"):
                    coder = line.split("=")[1].strip()
    except FileNotFoundError:
        print(f"{colors.RED}:: Error - File 'version' not found.{colors.END}")
    except Exception as e:
        print(f"{colors.RED}:: Error - Occurred while reading 'version': {str(e)}{colors.END}")
    return version, coder

version, coder = read_version_and_coder()
if version is None or coder is None:
    exit()

interval = 20

def git_pull(path, remote="origin", branch="master"):
    try:
        os.chdir(path)  # Change directory to the repository path
        os.system(f"git pull {remote} {branch}")
    except Exception as e:
        print(f"{colors.RED}:: Error - Occurred while pulling updates in path {path}: {str(e)}{colors.END}")

def main():

    # Signal handler for Ctrl+C
    def signal_handler(sig, frame):
        print(f"\n{colors.YELLOW}:: Exiting the program...{colors.END}")
        exit(0)

    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Print ASCII banner
    print(colors.DARK_RED + banner + colors.END)

    # Print coder and version in different colors
    if version is not None and coder is not None:
        print(f"{colors.YELLOW}Coder: {coder:<50}{colors.GREEN}{version:>27}{colors.END}\n")
    else:
        print(f"{colors.RED}:: Error - Version or coder not found.{colors.END}")
        exit()

    # Read paths and URLs from JSON file
    try:
        with open("paths_and_urls.json") as file:
            data = json.load(file)
            repositories = data["repositories"]
    except FileNotFoundError:
        print(f"{colors.RED}:: Error - File 'paths_and_urls.json' not found.{colors.END}")
        return

    # Dictionary to store last update times
    last_update_times = {}

    while True:
        print("Checking for repository updates...")

        # Initialize last_update_times if it's empty
        if not last_update_times:
            for repo in repositories:
                last_update_times[repo["repository"]] = ""

        for repo in repositories:
            try:
                username = repo["username"]
                repository = repo["repository"]
                remote = repo["remote"]
                branch = repo["branch"]
                url = f"https://codeberg.org/api/v1/repos/{username}/{repository}"
                
                # Fetch repository data
                response = requests.get(url)
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
                
                # Process response
                repo_data = response.json()
                if repo_data:  # Check if repo_data is not None
                    last_update_time = repo_data.get("updated_at")
                    if last_update_time and last_update_times.get(repository) != last_update_time:
                        # Repository has been updated, pull changes
                        path = repo["path"]
                        git_pull(path, remote, branch)
                        last_update_times[repository] = last_update_time
                        print(f"{colors.GREEN}Updated repository: {username}/{repository}.{colors.END}")
                else:
                    print(f"{colors.RED}:: Error - Empty JSON response while checking repository {username}/{repository}.{colors.END}")

            except HTTPError as http_err:
                if response.status_code == 404:
                    error_data = response.json()
                    if error_data.get("message") == "The target couldn't be found.":
                        print(f"{colors.RED}:: Error - Repository not found: {username}/{repository}.{colors.END}")
                        exit(0)
                    elif error_data.get("message") == "GetUserByName":
                        print(f"{colors.RED}:: Error - Username not found: {username}/{repository}.{colors.END}")
                        exit(0)
                    else:
                        print(f"{colors.RED}:: Error - Unknown HTTP error occurred: {http_err}{colors.END}")
                        exit(0)

            except RequestException as req_err:
                print(f"{colors.RED}:: Error - Request exception occurred: {req_err}{colors.END}")

            except Exception as e:
                print(f"{colors.RED}:: Error - Error occurred while checking repository {username}/{repository}: {str(e)}{colors.END}")

        print("Waiting for next check...")
        time.sleep(interval)

if __name__ == "__main__":
    main()
