# scripts/chunk.py
# Split cleaned text files into chunks with metadata and save as JSON in data/chunks/
import os
import glob
import json

# Parameters
CHUNK_SIZE = 1500  # characters per chunk (adjust as needed)
# DIRECTORIES
tmp = os.path.dirname(__file__)
CLEAN_DIR = os.path.abspath(os.path.join(tmp, os.pardir, 'data', 'cleaned'))
CHUNK_DIR = os.path.abspath(os.path.join(tmp, os.pardir, 'data', 'chunks'))

# Ensure output directory exists
os.makedirs(CHUNK_DIR, exist_ok=True)

# Iterate over each cleaned text file
for txt_path in glob.glob(os.path.join(CLEAN_DIR, '*.txt')):
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Base name for metadata
    base_name = os.path.splitext(os.path.basename(txt_path))[0]
    start = 0
    chunk_index = 0

    # Continue until we've processed the entire text
    while start < len(text):
        # Determine end index for this chunk
        end = start + CHUNK_SIZE
        # If we're not at the end, try to cut at the last whitespace for clean boundary
        if end < len(text):
            segment = text[start:end]
            last_space = segment.rfind(' ')
            if last_space != -1:
                end = start + last_space

        # Extract the chunk text
        chunk_text = text[start:end].strip()

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

        print(f"Saved chunk {chunk_index} for {base_name}")

        # Prepare for next chunk
        chunk_index += 1
        start = end

print("Chunking complete!")
