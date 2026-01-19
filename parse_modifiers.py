import re

def parse_error_log(file_path):
    """
    Parse the error.log file and extract modifier names that threw errors.
    
    Args:
        file_path (str): Path to the error.log file
        
    Returns:
        list: List of modifier names that caused errors
    """
    modifiers = []
    
    # Pattern to match modifier names in error messages
    # Looking for: Modifier 'modifier_name' doesn't match expected type
    pattern = r"Modifier '([^']+)' doesn't match expected type"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.search(pattern, line)
                if match:
                    modifier_name = match.group(1)
                    modifiers.append(modifier_name)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
    
    return modifiers

def load_existing_modifiers(output_path):
    """Load existing modifiers from the output file if it exists."""
    existing_modifiers = set()
    try:
        with open(output_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:  # Skip empty lines
                    existing_modifiers.add(line)
    except FileNotFoundError:
        pass  # File doesn't exist yet, that's fine
    except Exception as e:
        print(f"Warning: Error reading existing modifiers file: {e}")
    
    return existing_modifiers

def main():
    # Path to the error.log file
    error_log_path = r"C:\Users\sared\Documents\Paradox Interactive\Crusader Kings III\logs\error.log"
    
    # Parse the log file
    modifiers = parse_error_log(error_log_path)
    
    # Save the list of modifiers to a file
    output_path = "invalid_modifiers.txt"
    
    # Load existing modifiers to avoid duplicates
    existing_modifiers = load_existing_modifiers(output_path)
    
    # Filter out modifiers that are already in the file
    new_modifiers = [mod for mod in modifiers if mod not in existing_modifiers]
    
    if not new_modifiers:
        print(f"No new modifiers to add. All {len(modifiers)} found modifiers are already in {output_path}")
        return
    
    try:
        # Append new modifiers to the file
        with open(output_path, 'a', encoding='utf-8') as file:
            for modifier in new_modifiers:
                file.write(modifier + '\n')
        
        total_modifiers = len(existing_modifiers) + len(new_modifiers)
        print(f"Successfully added {len(new_modifiers)} new modifiers to {output_path}")
        print(f"Total modifiers in file: {total_modifiers}")
    except Exception as e:
        print(f"Error saving to file: {e}")

if __name__ == "__main__":
    main()