# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv


@click.command()
@click.option('--num-samples', default=100000, help='Number of reviews to process')
@click.option('--min-stars', default=3, help='Minimum star rating filter')
def main(num_samples, min_stars):
    """Process raw Yelp data into analysis-ready format.
    
    This script combines sampling and merging operations:
    1. Filters reviews with >= min_stars rating
    2. Merges business categories with reviews
    3. Outputs a single processed dataset
    
    Usage:
        python -m src.data.make_dataset
        python -m src.data.make_dataset --num-samples 50000 --min-stars 4
    """
    logger = logging.getLogger(__name__)
    logger.info('Processing Yelp review data...')
    
    # Import here to avoid circular dependencies
    from prepare_review_data import prepare_review_dataset
    
    project_dir = Path(__file__).resolve().parents[2]
    review_file = project_dir / 'data/raw/yelp_academic_dataset_review.json'
    business_file = project_dir / 'data/raw/yelp_academic_dataset_business.json'
    output_file = project_dir / 'data/processed/review_business_data.jsonl'
    
    logger.info(f'Input: {review_file.name}')
    logger.info(f'Output: {output_file}')
    logger.info(f'Parameters: num_samples={num_samples}, min_stars={min_stars}')
    
    prepare_review_dataset(
        str(review_file), 
        str(business_file), 
        str(output_file),
        num_samples=num_samples,
        min_stars=min_stars
    )
    
    logger.info('☑ Data processing complete')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
