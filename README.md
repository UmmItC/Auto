# AutoGitPull

AutoGitPull is a Python script that automates the process of pulling updates from Git repositories at specified intervals.

## Features

- Automatically pulls updates from multiple Git repositories.
- Configurable interval for pulling updates.

## Requirements

- Python 3.x
- Git (installed and configured)

## Usage

1. Clone this repository to your local machine:

    ```bash
    git clone https://codeberg.org/UmmIt/AutoGitPull.git
    ```

2. Navigate to the project directory:

    ```bash
    cd AutoGitPull
    ```
3. Edit JSON file which is called `paths_and_urls.json` with the following structure:

    ```json
    {
        "repositories": [
            {
                "username": "username",
                "repository": "repository_name",
                "path": "~/Documents/repository_name",
                "path_chdir": "~/Documents/"
                "remote": "origin",
                "branch": "master"
            },
            {
                "username": "username",
                "repository": "repository_name",
                "path": "~/Documents/repository_name",
                "path_chdir": "~/Documents/"
                "remote": "origin",
                "branch": "master"
            }
        ]
    }
    ```

Replace `username` with your Codeberg username, `repository` with the name of your repository, and `/path/of/your/repository` with the actual path to your repository.

5. Run the script:

    ```bash
    python3 git_pull_script.py
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.
