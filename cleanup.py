# List of non-kids-friendly terms to remove
non_kids_friendly_terms = [
    "セックス", "コンドーム", "ポルノ", "ナチズム", "ナチ", "ダッチワイフ",
    "マゾ", "サディスト", "ブルセラ", "エロ", "エロス", "シュックスナイン",
    "ラーゲ", "ホモ", "レズ", "ヘルス", "アダルトビデオ", "シックスナイン",
    "セクハラ", "テレクラ", "ローション", "ソープランド"
]

# File paths
input_file = "D:/Personal Stuff/Nihongo/07_Software/code_collection/aoi/words.txt"  # Replace with your input file name
output_file = "D:/Personal Stuff/Nihongo/07_Software/code_collection/aoi/words.txt"  # Replace with your desired output file name

# Read the input file
with open(input_file, "r", encoding="utf-8") as file:
    lines = file.readlines()

# Filter out non-kids-friendly terms
filtered_lines = [
    line for line in lines
    if not any(term in line for term in non_kids_friendly_terms)
]

# Write the filtered list to a new file
with open(output_file, "w", encoding="utf-8") as file:
    file.writelines(filtered_lines)

print(f"Filtered list saved to {output_file}")
