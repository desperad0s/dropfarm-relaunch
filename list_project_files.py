import os

# Define directories to exclude
EXCLUDE_DIRS = {'node_modules', '.git', 'venv', '__pycache__', '.svelte-kit'}

def list_files_and_contents(directory, output_file):
    with open(output_file, 'w', encoding='utf-8') as out_file:
        for root, dirs, files in os.walk(directory):
            # Exclude specified directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                file_path = os.path.join(root, file)
                out_file.write(f"// {file_path}\n")
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        out_file.write(f.read())
                except Exception as e:
                    out_file.write(f"Error reading {file_path}: {e}\n")
                out_file.write("----------------------------------------------------------------------------------\n")

# Specify the output file
output_file = 'project_structure.md'

# Start from the current directory
list_files_and_contents('.', output_file)

print(f"Project structure and contents have been logged to {output_file}")