"""
Compare association rule mining algorithms with different minimum support thresholds.

This script runs multiple mining algorithms (Apriori, FP-Growth, Weighted Apriori)
with various minimum support values and compares their performance.
"""

import pandas as pd
import warnings
from pathlib import Path
import json
from typing import Dict, List

from src.models.mining_strategies import (
    AprioriStrategy,
    FPGrowthStrategy,
    WeightedAprioriStrategy,
    MiningContext
)

warnings.filterwarnings("ignore", category=DeprecationWarning)


def load_transaction_data(data_dir: Path):
    """Load preprocessed transaction data.
    
    Args:
        data_dir: Directory containing processed data files
        
    Returns:
        Tuple of (encoded_df, transactions_list)
    """
    print("Loading transaction data...")
    
    # Load one-hot encoded data for Apriori/FP-Growth
    encoded_path = data_dir / 'transactions_encoded.csv'
    df_encoded = pd.read_csv(encoded_path)
    
    # Load raw transactions for Weighted Apriori
    transactions_path = data_dir / 'user_transactions.pkl'
    user_transactions = pd.read_pickle(transactions_path)
    transactions_list = user_transactions['transaction_items'].tolist()
    
    print(f"  ☑ Loaded {len(transactions_list)} transactions")
    print(f"  ☑ Unique categories: {df_encoded.shape[1]}")
    
    return df_encoded, transactions_list


def run_algorithm_comparison(df_encoded: pd.DataFrame, 
                             transactions_list: List,
                             min_support_values: List[float]) -> Dict:
    """Run all algorithms with different minimum support values.
    
    Args:
        df_encoded: One-hot encoded transaction data
        transactions_list: List of transaction sets
        min_support_values: List of minimum support thresholds to test
        
    Returns:
        Dictionary containing results for all algorithms
    """
    results = {
        'apriori': {'minsup': [], 'time': [], 'itemsets_count': [], 'itemset_sizes': []},
        'fpgrowth': {'minsup': [], 'time': [], 'itemsets_count': [], 'itemset_sizes': []},
        'weighted': {'minsup': [], 'time': [], 'itemsets_count': [], 'itemset_sizes': []}
    }
    
    print(f"\n{'='*80}")
    print("RUNNING ALGORITHM COMPARISON")
    print(f"{'='*80}")
    print(f"Minimum support values: {min_support_values}\n")
    
    # Run Apriori
    print("Running Apriori...")
    context = MiningContext(AprioriStrategy())
    for minsup in min_support_values:
        frequent_itemsets, exec_time = context.execute_mining(df_encoded, minsup)
        itemsets_count = len(frequent_itemsets)
        
        # Calculate itemset size distribution
        itemset_sizes = {}
        for _, row in frequent_itemsets.iterrows():
            size = len(row['itemsets'])
            itemset_sizes[size] = itemset_sizes.get(size, 0) + 1
        
        results['apriori']['minsup'].append(minsup)
        results['apriori']['time'].append(exec_time)
        results['apriori']['itemsets_count'].append(itemsets_count)
        results['apriori']['itemset_sizes'].append(itemset_sizes)
        
        print(f"  minsup={minsup:.3f}: {exec_time:.4f}s, {itemsets_count} itemsets")
    
    # Run FP-Growth
    print("\nRunning FP-Growth...")
    context.strategy = FPGrowthStrategy()
    for minsup in min_support_values:
        frequent_itemsets, exec_time = context.execute_mining(transactions_list, minsup)
        itemsets_count = len(frequent_itemsets)
        
        # Calculate itemset size distribution
        itemset_sizes = {}
        for itemset, _ in frequent_itemsets:
            size = len(itemset)
            itemset_sizes[size] = itemset_sizes.get(size, 0) + 1
        
        results['fpgrowth']['minsup'].append(minsup)
        results['fpgrowth']['time'].append(exec_time)
        results['fpgrowth']['itemsets_count'].append(itemsets_count)
        results['fpgrowth']['itemset_sizes'].append(itemset_sizes)
        
        print(f"  minsup={minsup:.3f}: {exec_time:.4f}s, {itemsets_count} itemsets")
    
    # Run Weighted Apriori
    print("\nRunning Weighted Apriori...")
    context.strategy = WeightedAprioriStrategy()
    for minsup in min_support_values:
        frequent_itemsets, exec_time = context.execute_mining(transactions_list, minsup)
        itemsets_count = len(frequent_itemsets)
        
        # Calculate itemset size distribution
        itemset_sizes = {}
        for itemset, _ in frequent_itemsets:
            size = len(itemset)
            itemset_sizes[size] = itemset_sizes.get(size, 0) + 1
        
        results['weighted']['minsup'].append(minsup)
        results['weighted']['time'].append(exec_time)
        results['weighted']['itemsets_count'].append(itemsets_count)
        results['weighted']['itemset_sizes'].append(itemset_sizes)
        
        print(f"  minsup={minsup:.3f}: {exec_time:.4f}s, {itemsets_count} itemsets")
    
    return results


def print_results_summary(results: Dict, num_transactions: int, num_categories: int):
    """Print formatted comparison results.
    
    Args:
        results: Results dictionary from algorithm comparison
        num_transactions: Total number of transactions
        num_categories: Total number of unique categories
    """
    print(f"\n{'='*80}")
    print("RESULTS SUMMARY")
    print(f"{'='*80}")
    
    # Create comparison DataFrame
    comparison_df = pd.DataFrame({
        'min_support': results['apriori']['minsup'],
        'apriori_time (s)': results['apriori']['time'],
        'fpgrowth_time (s)': results['fpgrowth']['time'],
        'weighted_time (s)': results['weighted']['time'],
        'apriori_itemsets': results['apriori']['itemsets_count'],
        'fpgrowth_itemsets': results['fpgrowth']['itemsets_count'],
        'weighted_itemsets': results['weighted']['itemsets_count'],
    })
    
    # Calculate speedup ratios
    comparison_df['apriori_vs_weighted'] = (
        comparison_df['apriori_time (s)'] / comparison_df['weighted_time (s)']
    )
    comparison_df['fpgrowth_vs_weighted'] = (
        comparison_df['fpgrowth_time (s)'] / comparison_df['weighted_time (s)']
    )
    
    print("\nComparison Table:")
    print(comparison_df.to_string(index=False))
    
    # Summary statistics
    print(f"\n{'-'*80}")
    print("SUMMARY STATISTICS")
    print(f"{'-'*80}")
    print(f"Total transactions: {num_transactions}")
    print(f"Total unique categories: {num_categories}")
    
    print(f"\nAverage execution times:")
    print(f"  Apriori:          {comparison_df['apriori_time (s)'].mean():.4f}s")
    print(f"  FP-Growth:        {comparison_df['fpgrowth_time (s)'].mean():.4f}s")
    print(f"  Weighted Apriori: {comparison_df['weighted_time (s)'].mean():.4f}s")
    
    print(f"\nAverage speedup ratios (vs Weighted Apriori):")
    avg_apriori_speedup = comparison_df['apriori_vs_weighted'].mean()
    avg_fpgrowth_speedup = comparison_df['fpgrowth_vs_weighted'].mean()
    
    print(f"  Apriori:   {avg_apriori_speedup:.2f}x")
    print(f"  FP-Growth: {avg_fpgrowth_speedup:.2f}x")
    
    return comparison_df


def save_results(results: Dict, comparison_df: pd.DataFrame, output_dir: Path):
    """Save results to files.
    
    Args:
        results: Raw results dictionary
        comparison_df: Comparison DataFrame
        output_dir: Directory to save results
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save comparison table
    comparison_path = output_dir / 'algorithm_comparison.csv'
    comparison_df.to_csv(comparison_path, index=False)
    print(f"\n✅ Saved comparison table to: {comparison_path}")
    
    # Save raw results as JSON
    results_path = output_dir / 'mining_results.json'
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✅ Saved raw results to: {results_path}")


def main():
    """Main execution function."""
    # Configuration
    project_dir = Path(__file__).resolve().parents[2]
    data_dir = project_dir / 'data/processed'
    output_dir = project_dir / 'models'
    
    # Minimum support values to test
    min_support_values = [0.2, 0.15, 0.1, 0.05, 0.02, 0.01]
    
    # Load data
    df_encoded, transactions_list = load_transaction_data(data_dir)
    
    # Run comparison
    results = run_algorithm_comparison(df_encoded, transactions_list, min_support_values)
    
    # Print and save results
    comparison_df = print_results_summary(
        results,
        len(transactions_list),
        df_encoded.shape[1]
    )
    
    save_results(results, comparison_df, output_dir)
    
    print(f"\n{'='*80}")
    print("TRAINING COMPLETE")
    print(f"{'='*80}")


if __name__ == '__main__':
    main()
