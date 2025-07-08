# scripts/preprocess.py
# Extract and clean main article text from raw HTML files into data/cleaned/

import os
import glob
import re
from bs4 import BeautifulSoup
from readability import Document

# Directories
script_dir = os.path.dirname(__file__)
RAW_DIR = os.path.abspath(os.path.join(script_dir, os.pardir, 'data', 'raw'))
CLEAN_DIR = os.path.abspath(os.path.join(script_dir, os.pardir, 'data', 'cleaned'))

os.makedirs(CLEAN_DIR, exist_ok=True)

# Get list of raw HTML files
html_files = glob.glob(os.path.join(RAW_DIR, "*.html"))

for html_path in html_files:
    try:
        # Read raw HTML
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()

        # Use Readability to extract main content
        doc = Document(html)
        summary_html = doc.summary()
        soup = BeautifulSoup(summary_html, 'html.parser')
        text = soup.get_text(separator=' ')

        # Normalize whitespace
        text = ' '.join(text.split())

        # Remove leading advertisements or boilerplate before the title
        TITLE_PHRASE = 'Hunza Valley'
        if TITLE_PHRASE in text:
            text = text[text.find(TITLE_PHRASE):]
        text = re.sub(r'-?\s*Advertisement[\s\S]*?(?=' + re.escape(TITLE_PHRASE) + ')', '', text)
        text = re.sub(r'Consider Purchasing[\s\S]*?(?=' + re.escape(TITLE_PHRASE) + ')', '', text)

        # Remove trailing advertisements or boilerplate after main content
        text = re.sub(r'-?\s*Advertisement[\s\S]*$', '', text)
        text = re.sub(r'Consider Purchasing[\s\S]*$', '', text)

        # Final whitespace normalization
        clean_text = ' '.join(text.split())

        # Write to file
        base = os.path.basename(html_path)
        name = os.path.splitext(base)[0] + '.txt'
        out_path = os.path.join(CLEAN_DIR, name)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(clean_text)

        print(f"Cleaned text saved: {out_path}")
    except Exception as e:
        print(f"Error processing {html_path}: {e}")
