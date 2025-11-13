"""
Transform processed review data into transaction format for association rule mining.

This script converts the review_business_data.jsonl into user-based transactions
where each transaction contains the unique business categories a user has reviewed.
"""

import json
import pandas as pd
import os
from pathlib import Path


def load_review_data(filepath):
    """Load processed review data from JSONL file.
    
    Args:
        filepath: Path to review_business_data.jsonl
        
    Returns:
        pandas DataFrame with columns: user_id, business_id, categories
    """
    print(f"Loading review data from: {filepath}")
    
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            record = json.loads(line)
            data.append({
                'user_id': record['user_id'],
                'business_id': record['business_id'],
                'categories': record['categories']
            })
    
    df = pd.DataFrame(data)
    print(f"  ☑ Loaded {len(df)} records")
    return df


def process_categories(df, filter_restaurant=True):
    """Process and clean category data.
    
    Args:
        df: DataFrame with categories column
        filter_restaurant: If True, keep only restaurant-related businesses
        
    Returns:
        DataFrame with processed categories
    """
    print("Processing categories...")
    
    # Drop rows with null or empty categories
    initial_count = len(df)
    df = df.dropna(subset=['categories'])
    df = df[df['categories'].str.strip() != '']
    
    print(f"  ☑ Removed {initial_count - len(df)} rows with invalid categories")
    
    # Optionally filter for restaurants
    if filter_restaurant:
        df = df[df['categories'].str.contains("Restaurant", case=False)]
        print(f"  ☑ Filtered to {len(df)} restaurant-related records")
    
    # Split categories into sets
    df['category_list'] = df['categories'].apply(
        lambda x: {cat.strip() for cat in x.split(',')}
    )
    
    return df


def create_user_transactions(df):
    """Group reviews by user and create transaction sets.
    
    Args:
        df: DataFrame with user_id and category_list columns
        
    Returns:
        DataFrame with columns: user_id, transaction_items
    """
    print("Creating user transactions...")
    
    user_transactions = df.groupby('user_id')['category_list'].agg(
        lambda sets: set().union(*sets)
    ).reset_index()
    
    user_transactions.columns = ['user_id', 'transaction_items']
    
    print(f"  ☑ Created {len(user_transactions)} user transactions")
    
    # Statistics
    avg_items = user_transactions['transaction_items'].apply(len).mean()
    print(f"  ☑ Average items per transaction: {avg_items:.2f}")
    
    return user_transactions


def encode_transactions(user_transactions):
    """Convert transaction sets to one-hot encoded DataFrame for Apriori.
    
    Args:
        user_transactions: DataFrame with transaction_items column
        
    Returns:
        One-hot encoded DataFrame suitable for mlxtend algorithms
    """
    print("Encoding transactions for association rule mining...")
    
    from mlxtend.preprocessing import TransactionEncoder
    
    transactions_list = user_transactions['transaction_items'].tolist()
    
    te = TransactionEncoder()
    te_ary = te.fit(transactions_list).transform(transactions_list)
    df_encoded = pd.DataFrame(te_ary, columns=te.columns_)
    
    print(f"  ☑ Encoded shape: {df_encoded.shape}")
    print(f"  ☑ Total unique categories: {df_encoded.shape[1]}")
    print(f"  ☑ Total transactions: {df_encoded.shape[0]}")
    
    return df_encoded, transactions_list


def build_transaction_features(input_file, output_dir, filter_restaurant=True):
    """Main pipeline to build transaction features from review data.
    
    Args:
        input_file: Path to review_business_data.jsonl
        output_dir: Directory to save processed transaction data
        filter_restaurant: Whether to filter for restaurants only
        
    Returns:
        Tuple of (encoded_df, transactions_list)
    """
    # Load and process data
    df = load_review_data(input_file)
    df = process_categories(df, filter_restaurant)
    user_transactions = create_user_transactions(df)
    df_encoded, transactions_list = encode_transactions(user_transactions)
    
    # Save outputs
    os.makedirs(output_dir, exist_ok=True)
    
    # Save one-hot encoded data
    encoded_path = os.path.join(output_dir, 'transactions_encoded.csv')
    df_encoded.to_csv(encoded_path, index=False)
    print(f"\n✅ Saved encoded transactions to: {encoded_path}")
    
    # Save raw transactions for weighted apriori
    transactions_path = os.path.join(output_dir, 'user_transactions.pkl')
    user_transactions.to_pickle(transactions_path)
    print(f"✅ Saved user transactions to: {transactions_path}")
    
    return df_encoded, transactions_list


def main():
    """Run the feature building pipeline."""
    project_dir = Path(__file__).resolve().parents[2]
    
    input_file = project_dir / 'data/processed/review_business_data.jsonl'
    output_dir = project_dir / 'data/processed'
    
    df_encoded, transactions_list = build_transaction_features(
        str(input_file),
        str(output_dir),
        filter_restaurant=True
    )
    
    print(f"\n{'='*80}")
    print("FEATURE BUILDING COMPLETE")
    print(f"{'='*80}")
    print(f"Transactions: {len(transactions_list)}")
    print(f"Unique categories: {df_encoded.shape[1]}")
    print(f"Sparsity: {(1 - df_encoded.sum().sum() / (df_encoded.shape[0] * df_encoded.shape[1])):.2%}")


if __name__ == '__main__':
    main()
