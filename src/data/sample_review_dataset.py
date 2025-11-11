import json
import os

def load_jsonl_sample(file_path, num_lines=100000):
    sample_data = []
    required_fields = ["review_id", "user_id", "business_id", "stars"]
    counter = 0

    with open(file_path, 'r', encoding='utf-8') as file:
        line = file.readline()
        while line and counter < num_lines:
            record = json.loads(line)
            if all(field in record for field in required_fields):
                if record["stars"] >= 3:  # Filter for reviews with more than 3 stars
                    sample_data.append({
                        "review_id": record["review_id"],
                        "user_id": record["user_id"],
                        "business_id": record["business_id"],
                    "stars": record["stars"]
                    })
                    counter += 1
            line = file.readline()

    # Save to new JSONL file
    with open('../../data/processed/sample_review_data.jsonl', 'w', encoding='utf-8') as json_file:
        for item in sample_data:
            json_file.write(json.dumps(item, ensure_ascii=False) + '\n')

    return sample_data

def main():
    # Define the path to the JSONL file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    jsonl_file_path = os.path.join(current_dir, '../../data/raw', 'yelp_academic_dataset_review.json')

    # Load and filter a sample of 1000 lines
    sample = load_jsonl_sample(jsonl_file_path, num_lines=100000)

    # Print confirmation
    print(f'Loaded and filtered {len(sample)} valid records into sample_review_data.jsonl.')


if __name__ == '__main__':
    main()