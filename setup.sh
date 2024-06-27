#!/bin/bash

# Define colors
COLOR_PROMPT="1;36"  # Cyan for prompts
COLOR_WARN="1;33"    # Yellow for warnings
COLOR_OK="1;32"      # Green for ok 

# Function to print colored prompt
print_prompt() {
    local message="$1"
    local color="$2"
    echo -e "\e[${color}m${message}\e[0m"
}

# Function to print colored warning
print_warning() {
    local message="$1"
    local color="$2"
    echo -e "\e[${color}m${message}\e[0m"
}

# Function to print colored ok
print_ok() {
    local message="$1"
    local color="$2"
    echo -e "\e[${color}m${message}\e[0m"
}

# Function to read input with a colored prompt and handle empty input
read_input() {
    local prompt_message="$1"
    local variable_name="$2"
    local color="$3"
    local default_value="${4:-}"  # Default value is empty if not provided

    while true; do
        if [[ -n "$default_value" ]]; then
            prompt_message="$prompt_message (default: $default_value)"
        fi
        print_prompt "${prompt_message}" "${color}"
        read -r -p "> " "${variable_name}"
        
        # If input is empty and default value is set, use default value
        if [[ -z "${!variable_name}" && -n "$default_value" ]]; then
            eval "$variable_name=\"$default_value\""
        fi

        if [[ -n "${!variable_name}" ]]; then
            break
        else
            print_warning "Input cannot be empty. Please enter a value." "${COLOR_WARN}"
        fi
    done
}

# Print prompts and read inputs with defaults for new_remote and new_branch
read_input "Enter new username (Codeberg username):" new_username "${COLOR_PROMPT}"
read_input "Enter new repository name (Repository name on Codeberg):" new_repository "${COLOR_PROMPT}"
read_input "Enter new path to change directory (Path to git clone):" new_path_chdir "${COLOR_PROMPT}"
read_input "Enter new path to the repository (Path to pulling repository):" new_path "${COLOR_PROMPT}"
read_input "Enter new remote name (Remote name of your repository):" new_remote "${COLOR_PROMPT}" "origin"
read_input "Enter new branch name (Branch name of your repository):" new_branch "${COLOR_PROMPT}" "master"

# Define the path to your JSON file
json_file="./settings.json"

# Update username
sed -i.bak 's/"username": "[^"]*"/"username": "'"$new_username"'"/' "$json_file"

# Update repository name
sed -i.bak 's/"repository": "[^"]*"/"repository": "'"$new_repository"'"/' "$json_file"

# Update path_chdir
sed -i.bak 's%"path_chdir": "[^"]*"%"path_chdir": "'"$new_path_chdir"'"%g' "$json_file"

# Update path
sed -i.bak 's%"path": "[^"]*"%"path": "'"$new_path"'"%g' "$json_file"

# Update remote
sed -i.bak 's/"remote": "[^"]*"/"remote": "'"$new_remote"'"/' "$json_file"

# Update branch
sed -i.bak 's/"branch": "[^"]*"/"branch": "'"$new_branch"'"/' "$json_file"

# Clean up backup file
rm "$json_file.bak"

# Display information in a table-like format
echo ""
printf "| %-20s | %-40s |\n" "Field" "Value"
printf "| %-20s | %-40s |\n" "------------------" "----------------------------------------"
printf "| %-20s | %-40s |\n" "Username" "$new_username"
printf "| %-20s | %-40s |\n" "Repository Name" "$new_repository"
printf "| %-20s | %-40s |\n" "Path Chdir" "$new_path_chdir"
printf "| %-20s | %-40s |\n" "Path to Repository" "$new_path"
printf "| %-20s | %-40s |\n" "Remote Name" "$new_remote"
printf "| %-20s | %-40s |\n" "Branch Name" "$new_branch"
echo ""

print_ok "[OK] JSON file updated successfully." "${COLOR_OK}"
print_ok "[OK] You can now Run python3 git_pull_script.py" "${COLOR_OK}"
