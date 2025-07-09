# scripts/chunk.py
# Split cleaned text files into overlapping chunks with metadata and save as JSON in data/chunks/
import os
import glob
import json

# Parameters
WORDS_PER_CHUNK = 200       # words per chunk
WORD_OVERLAP = 50           # words to overlap between chunks

# Directories
BASE_DIR = os.path.dirname(__file__)
CLEAN_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir, 'data', 'cleaned'))
CHUNK_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir, 'data', 'chunks'))

# Ensure output directory exists
os.makedirs(CHUNK_DIR, exist_ok=True)

# Iterate over each cleaned text file
for txt_path in glob.glob(os.path.join(CLEAN_DIR, '*.txt')):
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split into words
    words = text.split()
    base_name = os.path.splitext(os.path.basename(txt_path))[0]
    total_words = len(words)
    start = 0
    chunk_index = 0

    # Create overlapping word-based chunks
    while start < total_words:
        end = start + WORDS_PER_CHUNK
        chunk_words = words[start:end]
        chunk_text = ' '.join(chunk_words)

        # Metadata
        chunk_data = {
            'id': f"{base_name}_chunk_{chunk_index}",
            'source': base_name,
            'position': chunk_index,
            'text': chunk_text
        }

        # Write chunk to JSON file
        out_file = os.path.join(CHUNK_DIR, f"{chunk_data['id']}.json")
        with open(out_file, 'w', encoding='utf-8') as out:
            json.dump(chunk_data, out, ensure_ascii=False, indent=2)

        print(f"Saved chunk {chunk_index} ({start}-{min(end,total_words)} words) for {base_name}")

        # Advance start by chunk size minus overlap
        chunk_index += 1
        start += WORDS_PER_CHUNK - WORD_OVERLAP

print("Chunking complete!")
