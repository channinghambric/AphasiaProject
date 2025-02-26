import csv
from functools import lru_cache
import nltk

# Ensure the CMU Pronouncing Dictionary is downloaded
try:
    nltk.corpus.cmudict.dict()
except LookupError:
    nltk.download('cmudict')

arpabet = nltk.corpus.cmudict.dict()

@lru_cache()
def count_phonemes(word):
    """
    Returns the number of phonemes in a given word based on the CMU Pronouncing Dictionary.

    Args:
        word (str): The word to analyze.

    Returns:
        int: The number of phonemes in the word, or None if not found.
    """
    word = word.lower()
    if word in arpabet:
        return len(arpabet[word][0])  # Use the first pronunciation variant
    return None  

def process_structured_txt_and_save_csv(txt_file, csv_file, delimiter="\t"):
    """
    Reads a text file with columns (ID, Entry), counts phonemes for each word in 'Entry',
    and saves results to a CSV file.

    Args:
        txt_file (str): Path to the input text file.
        csv_file (str): Path to save the output CSV file.
        delimiter (str): Delimiter used in the text file (default is tab '\t' for TSV files).
    """
    results = []

    with open(txt_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=delimiter) 
        for row in reader:
            word = row["Entry"].strip()  # Get the word from "Entry" column
            phoneme_count = count_phonemes(word)
            results.append([row["ID"], word, phoneme_count])  # Store 

    # Save results to a CSV file
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Entry", "Phoneme Count"])  
        writer.writerows(results) 

    print(f"Phoneme counts saved to {csv_file}")

# Example usage
txt_file = "pwa_fluency_cleaned.txt"   
csv_file = "pwa_wordlength.csv"  
process_structured_txt_and_save_csv(txt_file, csv_file)
