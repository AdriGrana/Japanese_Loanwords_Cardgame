import os
import json
import unicodedata

# Function to check if a word is written in katakana
def is_katakana(word):
    return all('KATAKANA' in unicodedata.name(char) for char in word if char.strip())

# Function to extract the first definition from nested structured content
def extract_first_definition(definitions):
    def find_first_string_content(obj):
        if isinstance(obj, dict):
            if 'content' in obj:
                value = obj['content']
                if isinstance(value, str):
                    return value
                else:
                    result = find_first_string_content(value)
                    if result:
                        return result
            for key, value in obj.items():
                result = find_first_string_content(value)
                if result:
                    return result
        elif isinstance(obj, list):
            for item in obj:
                result = find_first_string_content(item)
                if result:
                    return result
        return None
    return find_first_string_content(definitions)

# Function to check if definitions contain source language information
def has_source_language(definitions):
    def search_for_source_language(obj):
        if isinstance(obj, dict):
            if obj.get('data', {}).get('content') == 'sourceLanguages':
                return True
            for key, value in obj.items():
                if search_for_source_language(value):
                    return True
        elif isinstance(obj, list):
            for item in obj:
                if search_for_source_language(item):
                    return True
        return False
    return search_for_source_language(definitions)

# Function to process a JSON file and extract entries
def process_json_file(file_path):
    results = []
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for entry in data:
            if len(entry) == 0:
                continue  # Skip empty entries

            japanese_word = entry[0]  # Japanese word

            # Check if English definitions exist
            english_definitions = entry[5] if len(entry) > 5 else None
            if not english_definitions:
                continue  # Skip if no definitions

            # Check for loanword indicators
            has_gai_tag = any(isinstance(elem, str) and "gai" in elem for elem in entry)
            is_katakana_word = is_katakana(japanese_word)
            has_source_lang = has_source_language(english_definitions)

            if has_gai_tag or is_katakana_word or has_source_lang:
                # Extract the first valid definition
                first_definition = extract_first_definition(english_definitions)
                if first_definition and isinstance(first_definition, str):
                    # Filter out redundant definitions
                    if first_definition != japanese_word and "（★）" not in first_definition:
                        results.append(f"{japanese_word}: {first_definition}")
        return results

# Main function to process all JSON files in a folder
def process_folder(folder_path, output_file):
    all_results = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            all_results.extend(process_json_file(file_path))
    
    # Write the results to a text file
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write("\n".join(all_results))
    print(f"Results written to {output_file}")

folder_path = "D:/Personal Stuff/Nihongo/07_Software/code_collection/aoi/jmdict"
output_file = "D:/Personal Stuff/Nihongo/07_Software/code_collection/aoi/words.txt"

process_folder(folder_path, output_file)
