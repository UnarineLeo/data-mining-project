import json
import os


def prepare_review_dataset(review_file, business_file, output_file, num_samples=100000, min_stars=3):
    """Sample reviews and merge with business categories in one pass.
    
    Args:
        review_file: Path to raw Yelp review JSON file
        business_file: Path to raw Yelp business JSON file
        output_file: Path to save processed output
        num_samples: Number of reviews to process (default: 100000)
        min_stars: Minimum star rating to include (default: 3)
    """
    
    # Load business categories into memory
    business_categories = {}
    print("Loading business data...")
    with open(business_file, 'r', encoding='utf-8') as bf:
        for line in bf:
            try:
                business = json.loads(line)
                if business.get("business_id") and business.get("categories"):
                    business_categories[business["business_id"]] = business["categories"]
            except json.JSONDecodeError:
                continue
    
    print(f"☑ Loaded {len(business_categories)} businesses with categories.")
    
    # Process reviews: filter, sample, and merge in one pass
    processed = 0
    skipped_stars = 0
    skipped_no_category = 0
    
    print(f"Processing reviews (target: {num_samples}, min stars: {min_stars})...")
    
    with open(review_file, 'r', encoding='utf-8') as rf, \
         open(output_file, 'w', encoding='utf-8') as out:
        
        for line in rf:
            if processed >= num_samples:
                break
                
            try:
                review = json.loads(line)
                
                # Filter by stars
                if review.get("stars", 0) < min_stars:
                    skipped_stars += 1
                    continue
                
                # Get business categories
                business_id = review.get("business_id")
                if not business_id:
                    continue
                    
                categories = business_categories.get(business_id)
                
                if not categories:
                    skipped_no_category += 1
                    continue
                
                # Create merged record
                merged_review = {
                    "review_id": review["review_id"],
                    "user_id": review["user_id"],
                    "business_id": business_id,
                    "stars": review["stars"],
                    "categories": categories
                }
                
                out.write(json.dumps(merged_review, ensure_ascii=False) + '\n')
                processed += 1
                
                # Progress indicator
                if processed % 10000 == 0:
                    print(f"  Processed {processed} reviews...")
                
            except (json.JSONDecodeError, KeyError):
                continue
    
    print(f"\n✅ Processing complete!")
    print(f"   Processed: {processed} reviews")
    print(f"   Skipped (low stars): {skipped_stars}")
    print(f"   Skipped (no category): {skipped_no_category}")
    print(f"   Output saved to: {output_file}")


def main():
    """Run the data preparation pipeline with default settings."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    review_file = os.path.join(current_dir, '../../data/raw', 'yelp_academic_dataset_review.json')
    business_file = os.path.join(current_dir, '../../data/raw', 'yelp_academic_dataset_business.json')
    output_file = os.path.join(current_dir, '../../data/processed', 'review_business_data.jsonl')
    
    prepare_review_dataset(review_file, business_file, output_file)


if __name__ == '__main__':
    main()
