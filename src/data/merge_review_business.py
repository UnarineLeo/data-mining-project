import json
import os

def merge_reviews_with_business_categories(review_file, business_file, output_file):
    # Load business data into a lookup dictionary: {business_id: categories}
    business_categories = {}
    with open(business_file, 'r', encoding='utf-8') as bf:
        for line in bf:
            try:
                business = json.loads(line)
                if business.get("business_id") and business.get("categories"):
                    business_categories[business["business_id"]] = business["categories"]
            except json.JSONDecodeError:
                continue

    print(f"Loaded {len(business_categories)} businesses with categories.")

    merged_data = []
    skipped = 0

    # Merge categories into each review record
    with open(review_file, 'r', encoding='utf-8') as rf, open(output_file, 'w', encoding='utf-8') as out:
        for line in rf:
            try:
                review = json.loads(line)
                business_id = review.get("business_id")
                if not business_id:
                    skipped += 1
                    continue

                categories = business_categories.get(business_id)
                if not categories:
                    skipped += 1
                    continue

                # Add categories to review record
                review["categories"] = categories
                out.write(json.dumps(review, ensure_ascii=False) + '\n')
                merged_data.append(review)

            except json.JSONDecodeError:
                skipped += 1
                continue

    print(f"Merged {len(merged_data)} records. Skipped {skipped} (no match or invalid JSON).")
    return merged_data


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    review_file = os.path.join(current_dir, '../../data/processed', 'sample_review_data.jsonl')
    business_file = os.path.join(current_dir, '../../data/raw', 'yelp_academic_dataset_business.json')
    output_file = os.path.join(current_dir, '../../data/processed', 'merged_review_business.jsonl')

    merged_data = merge_reviews_with_business_categories(review_file, business_file, output_file)

    print(f"✅ Merged file saved to: {output_file}")
    print(f"Total merged entries: {len(merged_data)}")


if __name__ == '__main__':
    main()
