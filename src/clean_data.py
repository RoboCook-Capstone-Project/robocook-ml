import csv 
import re
# Words & Regex
words_to_delete = ["gram", "kilo", "kg", "liter", "ons", "ml",
                   "potong", "ptg", "buah", "bh", "butir", "btr", "sachet", "gls",
                   "sedikit", "secukupnya", "sckpnya", "secukup nya", "se cukupnya", "secukup",
                   "sdm", "sdt", "sct", "siung", "batang", "btg", "lembar", "lbr", "lb", "cup",
                   "segenggam", "genggam", "sejumput", "se jumput", "jumput", "bj",
                   "sendok makan", "sendok teh", "sendok", "seikat", "ikat", "sck",
                   "seruas jari", "ruas jari", "seruas", "ruas", "bungkus", "bks", 
                   "sepiring", "piring", "biji", "sesuai selera", "tangkai"]
                    # Manual: ekor
standalone_words = ['g', "gr"]
emojis = re.compile("["
                           "\U0001F600-\U0001F64F"  # Emoticons
                           "\U0001F300-\U0001F5FF"  # Symbols & pictographs
                           "\U0001F680-\U0001F6FF"  # Transport & map symbols
                           "\U0001F700-\U0001F77F"  # Alchemical symbols
                           "\U0001F780-\U0001F7FF"  # Geometric shapes
                           "\U0001F800-\U0001F8FF"  # Miscellaneous symbols
                           "\U0001F900-\U0001F9FF"  # Supplemental symbols and pictographs
                           "\U0001FA00-\U0001FA6F"  # Extended-A
                           "\U0001FA70-\U0001FAFF"  # Extended-B
                           "\U00002702-\U000027B0"  # Dingbats
                           "\U000024C2-\U0001F251" 
                           "]+", flags=re.UNICODE)

def clean_regex(word):
    # Delete numbers with hyphens in between them (2-3, 45-90, etc)
    cleaned_word = re.sub(r'(\d)-(\d)', '', word)
    # Delete numbers
    cleaned_word = re.sub(r'\b(?:\d+/\d+|\d+)\b', '', cleaned_word)
    # Delete anything with parentheses
    cleaned_word = re.sub(r'\([^)]*\)', '', cleaned_word)
    # Delete emojis
    cleaned_word = emojis.sub('', cleaned_word)
    # Delete more or less
    cleaned_word = re.sub(r'\+\-|\-\+', '', cleaned_word)
    # Delete astrix
    cleaned_word = cleaned_word.replace('*', '')

    for delete_word in words_to_delete:
        cleaned_word = cleaned_word.replace(delete_word, '')
    
    for standalone_word in standalone_words:
        # Standalone words such as gr to avoid sangrai become sanai
        standalone_regex = rf'(?<!\S){re.escape(standalone_word)}(?!\S)'
        cleaned_word = re.sub(standalone_regex, '', cleaned_word, flags=re.IGNORECASE)
    # Delete space between slashes
    cleaned_word = re.sub(r'\s*/\s*', '/', cleaned_word)
    cleaned_word = re.sub(r'\s*--\s*', '--', cleaned_word)
    return cleaned_word.strip()

def update_ingredients(rows, input_file, ingredients_only):
    with open(input_file, 'r', encoding="utf8") as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        if (not ingredients_only):
            header.append("Main_Ingredient")
            rows.append(header)
        
        for row in csvreader: 
            # Delete unnecessary words on ingredients column
            cleaned_ingredients = clean_regex(row[1].lower())
            row[1] = cleaned_ingredients
            if (ingredients_only):
                rows.append(cleaned_ingredients)
            else: 
                rows.append(row)
    return rows 

if __name__ == "__main__": 
    dataset = input("Dataset: ")
    ingredients_only = False # Set True for testing (CSV will only contain ingredient column)
    input_file = f'./data/raw/dataset-{dataset}.csv'
    rows = update_ingredients([], input_file, ingredients_only)
    if (not ingredients_only):
        for row in rows[1:]:
            row.append(dataset)

    output_file = f'./data/cleaned/dataset-{dataset}-cleaned.csv'
    with open(output_file, 'w', newline='', encoding='utf8') as file: 
        csvwriter = csv.writer(file)
        if (ingredients_only):
            for row in rows:
                csvwriter.writerow([row])
        else: 
            csvwriter.writerows(rows)