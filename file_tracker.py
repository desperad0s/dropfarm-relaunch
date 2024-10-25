import os
import hashlib
import json
from typing import Dict, Set
from datetime import datetime

# Define directories to exclude
EXCLUDE_DIRS = {'node_modules', '.git', 'venv', '__pycache__', '.svelte-kit'}
EXCLUDE_FILES = {'package-lock.json', 'yarn.lock', '*.png', '*.jpg', '*.ico'}

def get_file_hash(file_path: str) -> str:
    """Calculate MD5 hash of a file."""
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def load_previous_state() -> tuple[Dict[str, str], bool]:
    """Load previous file hashes from state file and determine if this is first run."""
    try:
        with open('.file_hashes.json', 'r') as f:
            data = json.load(f)
            return data.get('hashes', {}), False
    except (FileNotFoundError, json.JSONDecodeError):
        return {}, True

def save_current_state(hashes: Dict[str, str]):
    """Save current file hashes to state file."""
    state = {
        'hashes': hashes,
        'last_updated': datetime.now().isoformat()
    }
    with open('.file_hashes.json', 'w') as f:
        json.dump(state, f, indent=2)

def get_all_files(directory: str) -> Set[str]:
    """Get all valid files in the directory."""
    valid_files = set()
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            if any(file.endswith(ext.replace('*', '')) for ext in EXCLUDE_FILES):
                continue
            
            file_path = os.path.join(root, file)
            valid_files.add(file_path)
    
    return valid_files

def write_file_contents(output_file, files_to_write: Set[str]):
    """Write contents of specified files to output file."""
    for file_path in sorted(files_to_write):
        output_file.write(f"// {file_path}\n")
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                output_file.write(f.read())
        except Exception as e:
            output_file.write(f"Error reading {file_path}: {e}\n")
        output_file.write("\n" + "-" * 80 + "\n")

def list_files_and_contents(directory: str):
    """Generate both full content and changes-only files."""
    previous_hashes, is_first_run = load_previous_state()
    current_hashes = {}
    changed_files = set()
    
    # Get all valid files
    all_files = get_all_files(directory)
    
    # Calculate current hashes and identify changes
    for file_path in all_files:
        try:
            current_hash = get_file_hash(file_path)
            current_hashes[file_path] = current_hash
            
            if not is_first_run and (file_path not in previous_hashes or previous_hashes[file_path] != current_hash):
                changed_files.add(file_path)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    # Generate full content file
    with open('project_structure.md', 'w', encoding='utf-8') as full_file:
        full_file.write("# Full Project Structure\n\n")
        write_file_contents(full_file, all_files)
    
    # Generate changes-only file if not first run and there are changes
    if not is_first_run and changed_files:
        with open('project_changes.md', 'w', encoding='utf-8') as changes_file:
            changes_file.write("# Changed Files\n\n")
            write_file_contents(changes_file, changed_files)
    elif is_first_run:
        print("Initial run - establishing baseline state. No changes file generated.")
    else:
        print("No changes detected since last run.")
    
    # Save current state for next comparison
    save_current_state(current_hashes)
    
    # Print summary
    print(f"Full project structure written to: project_structure.md")
    if not is_first_run:
        if changed_files:
            print(f"Changes written to: project_changes.md")
            print(f"Number of changed files: {len(changed_files)}")
        else:
            print("No changes detected - project_changes.md not created")

if __name__ == "__main__":
    list_files_and_contents('.')