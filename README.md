# AutoGitPull

AutoGitPull is a Python script that automates the process of pulling updates from Git repositories at specified intervals.

## Features

- Automatically pulls updates from multiple Git repositories.
- Configurable interval for pulling updates.
- User-friendly terminal interface with commands to list available commands, pull updates, and exit the program.

## Requirements

- Python 3.x
- Git (installed and configured)

## Usage

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/UmmIt/AutoGitPull.git
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
                "path": "/path/to/repository1",
                "url": "https://github.com/your_username/repository1.git"
            },
            {
                "path": "/path/to/repository2",
                "url": "https://github.com/your_username/repository2.git"
            },
            ...
        ]
    }
    ```

    Replace `/path/to/repository1`, `/path/to/repository2`, etc., with the local paths to your Git repositories, and replace `https://github.com/your_username/repository1.git`, `https://github.com/your_username/repository2.git`, etc., with the URLs of your Git repositories.

5. Run the script:

    ```bash
    python3 AutoGitPull.py
    ```

6. Follow the instructions in the terminal to interact with the script (e.g., type `help` to list available commands, `pull` to pull updates from the Git repositories, `exit` to exit the program).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
