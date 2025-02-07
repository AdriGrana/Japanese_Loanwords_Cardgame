#!/usr/bin/env python
# -*- coding: utf-8 -*-

def load_definitions(filename):
    """Read a file with lines in the format 'word: definition'
       and return a dictionary {word: definition}.
    """
    definitions = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # skip empty lines
            if ':' not in line:
                continue  # skip lines that do not have a colon
            # Split only on the first colon
            word, definition = line.split(':', 1)
            definitions[word.strip()] = definition.strip()
    return definitions

def main():
    # File names (assumed to be in the same directory as the script)
    mono_file = 'words_monolingual.txt'
    eng_file = 'words.txt'
    output_file = 'words_combined.txt'

    # Load both definitions into dictionaries.
    mono_defs = load_definitions(mono_file)
    eng_defs = load_definitions(eng_file)

    # Create a new dictionary that replaces missing definitions
    combined_defs = {}
    for word, mono_def in mono_defs.items():
        # If the monolingual definition is exactly "【定義が見つかりません】"
        if mono_def == "【定義が見つかりません】":
            # Look for an english definition (if not found, leave as is)
            combined_defs[word] = eng_defs.get(word, mono_def)
        else:
            combined_defs[word] = mono_def

    # Write the combined definitions to a new file.
    with open(output_file, 'w', encoding='utf-8') as out:
        for word, definition in combined_defs.items():
            out.write(f"{word}: {definition}\n")

    print(f"Combined definitions written to {output_file}")

if __name__ == '__main__':
    main()
