import os
import json
import glob

def extract_text(item):
    """
    Recursively extract text from a structured JSON item.
    If the item is a string, return it.
    If it is a list, process each element.
    If it is a dict and has a "content" key, process that.
    """
    if isinstance(item, str):
        return item
    elif isinstance(item, list):
        return ''.join(extract_text(elem) for elem in item)
    elif isinstance(item, dict):
        # Some objects have both "data" and "content" keys.
        if 'content' in item:
            return extract_text(item['content'])
        else:
            return ''
    else:
        return ''

def get_definition_from_entry(entry):
    """
    Given one dictionary entry from the 大辞林 JSON (which is a list),
    extract the definition text.
    
    In our sample entry the definition information is stored at index 5
    as a list of "senses" (each of which is a structured content object).
    """
    if len(entry) > 5 and isinstance(entry[5], list):
        definition_parts = []
        for sense in entry[5]:
            # Extract all text from the sense object.
            definition_parts.append(extract_text(sense))
        return ' '.join(definition_parts).strip()
    return ''

def build_index(daijirin_folder):
    """
    Look for JSON files in daijirin_folder that begin with "term_bank" and
    build a lookup dictionary where the keys are the headword (and reading)
    and the values are the monolingual definition.
    
    (You can later extend this to include alternative forms.)
    """
    index = {}
    json_files = glob.glob(os.path.join(daijirin_folder, 'term_bank*.json'))
    for file_path in json_files:
        print(f"Loading {os.path.basename(file_path)} ...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            continue

        for entry in data:
            # Skip if entry is empty or badly formed.
            if not entry or len(entry) < 1:
                continue
            # The first element is the headword.
            headword = entry[0]
            definition = get_definition_from_entry(entry)
            if headword and headword not in index:
                index[headword] = definition
            # Also try indexing by the reading (element at index 1) if available.
            if len(entry) > 1:
                reading = entry[1]
                if reading and reading not in index:
                    index[reading] = definition
    return index

def main():
    # Determine the directory of this script.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Files are assumed to be in the same directory as the script.
    words_file = os.path.join(base_dir, 'words.txt')
    output_file = os.path.join(base_dir, 'words_monolingual.txt')
    
    # The daijirin JSON files are in the subfolder "daijirin".
    daijirin_folder = os.path.join(base_dir, 'daijirin')
    
    print("Building dictionary index from daijirin JSON files...")
    dict_index = build_index(daijirin_folder)
    print("Index built with", len(dict_index), "entries.")
    
    # Read your original words.txt and process line by line.
    output_lines = []
    with open(words_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Expecting format: <word>: <english definition>
            if ':' in line:
                word, _ = line.split(":", 1)
                word = word.strip()
            else:
                word = line.strip()
            
            # Look up the word in our dictionary index.
            # (If nothing is found, you can change the default message.)
            definition = dict_index.get(word, "【定義が見つかりません】")
            output_lines.append(f"{word}: {definition}")
    
    # Write out the new file.
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(output_lines))
    
    print(f"Monolingual definitions written to {output_file}")

if __name__ == "__main__":
    main()
