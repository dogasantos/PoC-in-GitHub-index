import json
import os
from datetime import datetime

# Path to the locally cloned PoC-in-GitHub repository (will be cloned by GitHub Action)
REPO_PATH = "PoC-in-GitHub"
OUTPUT_FILE = "poc_index.json"
BASE_RAW_URL = "https://raw.githubusercontent.com/nomi-sec/PoC-in-GitHub/master"

def generate_index_local( ):
    """
    Traverses the local PoC-in-GitHub repository and creates a lightweight index
    mapping CVE ID to the raw URL of its corresponding JSON file.
    """
    print(f"[{datetime.now()}] Starting local index generation...")
    
    if not os.path.isdir(REPO_PATH):
        print(f"[{datetime.now()}] Error: Repository path not found at {REPO_PATH}")
        exit(1)
        
    poc_index = {}
    file_count = 0
    
    # Traverse the repository directory
    for root, _, files in os.walk(REPO_PATH):
        for file in files:
            if file.endswith(".json") and file.startswith("CVE-"):
                file_path_relative = os.path.relpath(os.path.join(root, file), REPO_PATH)
                file_count += 1
                
                cve_id = file.replace(".json", "")
                raw_url = f"{BASE_RAW_URL}/{file_path_relative}"
                
                poc_index[cve_id] = raw_url

    print(f"[{datetime.now()}] Finished traversing {file_count} files.")
    print(f"[{datetime.now()}] Index created. Total unique CVEs with PoCs: {len(poc_index)}")
    
    # Save the index to a JSON file
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(poc_index, f, indent=2)
        
    print(f"[{datetime.now()}] Index saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_index_local()
