# AutoGitPull

AutoGitPull is a Python script designed to automate the synchronization of code from Git repositories when updates are detected.

## Requirements

- Python 3.x
- Git (installed and configured)

## Usage

1. **Clone the Repository:**

   ```bash
   git clone https://codeberg.org/your_username/AutoGitPull.git
   cd AutoGitPull
   ```

2. **Edit `settings.json`:**

   Edit the `settings.json` file with your repository details. Here is an example structure:

   ```json
   {
       "repositories": [
           {
               "username": "your_codeberg_username",
               "repository": "your_repository_name",
               "path": "/path/to/your/repository",  // Path for 'git pull'
               "path_chdir": "/path/to/your/repository",  // Path for 'git clone' if not existing
               "remote": "origin",
               "branch": "master"
           },
           {
               "username": "another_codeberg_username",
               "repository": "another_repository_name",
               "path": "/path/to/another/repository",  // Path for 'git pull'
               "path_chdir": "/path/to/another/repository",  // Path for 'git clone' if not existing
               "remote": "origin",
               "branch": "main"
           }
       ]
   }
   ```

   - **username**: Replace `"your_codeberg_username"` and `"another_codeberg_username"` with your actual Codeberg usernames.
   - **repository**: Replace `"your_repository_name"` and `"another_repository_name"` with the names of your repositories.
   - **path**: Specify the path where the repository is located. This path is used for `git pull` to update the repository.
   - **path_chdir**: Specify the path where the repository will be cloned if it doesn't exist locally. This path is used for `git clone` when the repository does not exist locally.
   - **remote**: The name of the remote repository (`origin` is standard).
   - **branch**: The branch name to pull updates from (e.g., `master`, `main`, etc.).

3. **Alternatively, Use `setup.sh`:**

   If you prefer not to manually edit `settings.json`, you can run `setup.sh` to configure your repositories interactively:

   ```bash
   ./setup.sh
   ```

   Follow the prompts to enter your Codeberg usernames, repository names, paths, remotes, and branches.

4. **Run the Script:**

   Execute the following command to start syncing updates from your configured repositories:

   ```bash
   python3 git_pull_script.py
   ```

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE.md) file for details.
