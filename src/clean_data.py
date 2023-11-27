import csv 
import re
#TODO: 
# Handle deskripsi tambahan seperti : 
    # udang windu lepaskan dari cangkangnya dan cuci bersih--tahu  dadu goreng setengah matang
    # --wortel, cincang halus--telur, kocok lepas
# Handle perbedaan singkatan seperti: 
    # daun bawang & daun bw
    # bw. merah & bawang merah
# Handle misspelling ? 
    # mrica, lada bitam, bawah putih, bawah merah, dst 
# Tambah words_to_delete kalo ada kata yang belum dimasukkin 
# Handle symbol-symbol seperti astrix (*), more or less (-+), emoji, dll


dataset = input("Dataset: ")
input_file = f'./data/raw/dataset-{dataset}.csv'

# Words & Regex
words_to_delete = ["gram", "kilo", "kg", "liter", "ons", "ml",
                   "potong", "ptg", "buah", "bh", "butir", "btr", "sachet", "gls",
                   "sedikit", "secukupnya", "sckpnya", "secukup nya", "se cukupnya", "secukup",
                   "sdm", "sdt", "sct", "siung", "batang", "btg", "lembar", "lbr", "lb", "cup",
                   "segenggam", "genggam", "sejumput", "se jumput", "jumput", "bj",
                   "sendok makan", "sendok teh", "sendok", "seikat", "ikat",
                   "seruas jari", "ruas jari", "ruas", "bungkus", "bks", 
                   "sepiring", "piring", "biji", "sesuai selera", "tangkai"]
                    # Manual: ekor
standalone_words = ['g', "gr"]
def clean_regex(word):
    # Delete numbers with hyphens in between them (2-3, 45-90, etc)
    cleaned_word = re.sub(r'(\d)-(\d)', '', word)
    # Delete numbers
    cleaned_word = re.sub(r'[\d/]', '', cleaned_word)
    # Delete anything with parentheses
    cleaned_word = re.sub(r'\([^)]*\)', '', cleaned_word)
    
    
    for delete_word in words_to_delete:
        cleaned_word = cleaned_word.replace(delete_word, '')
    
    for standalone_word in standalone_words:
        # Standalone words such as gr to avoid sangrai become sanai
        standalone_regex = rf'(?<!\S){re.escape(standalone_word)}(?!\S)'
        cleaned_word = re.sub(standalone_regex, '', cleaned_word, flags=re.IGNORECASE)


    cleaned_word = re.sub(r'\s*--\s*', '--', cleaned_word)
    return cleaned_word.strip()




rows = []
with open(input_file, 'r', encoding="utf8") as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    rows.append(header)
    for row in csvreader: 
        # Delete unnecessary words on ingredients column
        cleaned_ingredients = clean_regex(row[1].lower())
        row[1] = cleaned_ingredients
        rows.append(row)

output_file = f'./data/cleaned/dataset-{dataset}-cleaned.csv'

with open(output_file, 'w', newline='', encoding='utf8') as file: 
    csvwriter = csv.writer(file)
    csvwriter.writerows(rows)