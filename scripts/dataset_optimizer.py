import json
import os
import time
import argparse
import random
import uuid
from multiprocessing import Pool, cpu_count
from typing import List, Dict

# Simulation of a large dataset size as mentioned in the resume
DATASET_SIZE = 230000
CHUNK_SIZE = 10000

def generate_dummy_annotation(index: int) -> Dict:
    """
    Generates a dummy annotation to simulate raw data.
    """
    return {
        "id": index,
        "image_id": f"img_{uuid.uuid4().hex[:8]}",
        "category": random.choice(["dress", "shirt", "pants", "skirt", "jacket"]),
        "bbox": [
            random.randint(0, 100),
            random.randint(0, 100),
            random.randint(100, 200),
            random.randint(100, 200)
        ],
        "attributes": {
            "color": random.choice(["red", "blue", "green", "black", "white"]),
            "pattern": random.choice(["solid", "striped", "dotted", "floral"])
        },
        "timestamp": time.time()
    }

def process_chunk(chunk_indices: List[int]) -> List[Dict]:
    """
    Process a chunk of data. This simulates the 'optimization' part
    where we might be converting formats, normalizing coordinates, etc.
    """
    processed_data = []
    for idx in chunk_indices:
        # Simulate reading raw data
        raw_item = generate_dummy_annotation(idx)
        
        # Simulate heavy processing / optimization logic
        # For example: Converting bbox format, mapping categories, etc.
        
        optimized_item = {
            "id": raw_item["id"],
            "image_path": f"s3://bucket/images/{raw_item['image_id']}.jpg",
            "label": raw_item["category"],
            "normalized_bbox": [
                raw_item["bbox"][0] / 256.0,
                raw_item["bbox"][1] / 256.0,
                raw_item["bbox"][2] / 256.0,
                raw_item["bbox"][3] / 256.0
            ],
            "metadata": raw_item["attributes"]
        }
        processed_data.append(optimized_item)
    return processed_data

def main():
    parser = argparse.ArgumentParser(description="Optimize 230K dataset annotations")
    parser.add_argument("--output", type=str, default="optimized_dataset.json", help="Output JSON file")
    parser.add_argument("--test-mode", action="store_true", help="Run with a smaller dataset for testing")
    args = parser.parse_args()

    total_records = 1000 if args.test_mode else DATASET_SIZE
    print(f"Starting dataset optimization for {total_records} records...")
    
    start_time = time.time()

    # Create chunks for multiprocessing
    indices = list(range(total_records))
    chunks = [indices[i:i + CHUNK_SIZE] for i in range(0, len(indices), CHUNK_SIZE)]

    print(f"Processing in {len(chunks)} chunks using {cpu_count()} cores...")

    with Pool(processes=cpu_count()) as pool:
        results = pool.map(process_chunk, chunks)

    # Flatten results
    final_dataset = [item for sublist in results for item in sublist]

    # Save to file
    with open(args.output, "w") as f:
        json.dump(final_dataset, f, indent=2)

    end_time = time.time()
    print(f"✅ Successfully optimized {len(final_dataset)} records in {end_time - start_time:.2f} seconds.")
    print(f"Saved to {args.output}")

if __name__ == "__main__":
    main()
