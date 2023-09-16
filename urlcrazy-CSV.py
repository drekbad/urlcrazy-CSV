import subprocess
import sys
import re

def run_urlcrazy(domain):
    try:
        output = subprocess.check_output(['urlcrazy', domain], text=True)
        return output.split('\n')
    except Exception as e:
        print(f"Error running urlcrazy: {e}")
        return None

def main():
    if len(sys.argv) > 1:
        domain = sys.argv[1]
    else:
        domain = input("Please enter the domain: ")

    lines = run_urlcrazy(domain)
    
    if lines is None:
        print("An error occurred while running urlcrazy.")
        return
    
    valid_typo_types = [
        "Character Omission", "Character Repeat", "Character Swap",
        "Character Replacement", "Double Replacement", "Character Insertion",
        "Missing Dot", "Insert Dash", "Singular or Pluralise",
        "Vowel Swap", "Homophones", "Homoglyphs", "Bit Flipping",
        "Wrong TLD", "All SLD", "Original"
    ]

    registered_lines = []
    unregistered_lines = []
    abrev_unreg_lines = []
    seen_typo_types = set()

    for line in lines:
        for typo_type in valid_typo_types:
            if line.startswith(typo_type):
                remaining = line[len(typo_type):].strip()
                parts = remaining.split()
                
                if not parts:
                    continue
                
                typo_domain = parts[0]
                ip = parts[1] if len(parts) > 1 else ''
                country = ' '.join(parts[2:]) if len(parts) > 2 else ''
                
                # Extract only the portion of country string before any extra data
                match = re.search(r"(.*\))", country)
                if match:
                    country = match.group(1)

                typo_type = typo_type.replace('Pluralise', 'Pluralize')

                if re.match(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", ip):
                    registered_lines.append(f"{typo_type},{typo_domain},{ip},{country}")
                elif typo_type not in ['Wrong TLD', 'All SLD']:
                    unregistered_lines.append(f"{typo_type},{typo_domain}")

                    if typo_type not in seen_typo_types:
                        abrev_unreg_lines.append(f"{typo_type},{typo_domain}")
                        seen_typo_types.add(typo_type)

    try:
        with open('REGISTERED.csv', 'w') as f:
            for line in registered_lines:
                f.write(line + '\n')

        with open('UNREGISTERED.csv', 'w') as f:
            for line in unregistered_lines:
                f.write(line + '\n')

        with open('ABREV-UNREG.csv', 'w') as f:
            for line in abrev_unreg_lines:
                f.write(line + '\n')

        print("The three output files have been successfully created.")
    except Exception as e:
        print(f"An error occurred while writing the output files: {e}")

if __name__ == '__main__':
    main()
