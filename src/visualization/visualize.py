"""
Visualize association rule mining algorithm comparison results.

This module creates plots and charts to compare the performance of
different mining algorithms.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json


def load_results(results_dir: Path):
    """Load comparison results from files.
    
    Args:
        results_dir: Directory containing results files
        
    Returns:
        Tuple of (comparison_df, results_dict)
    """
    comparison_path = results_dir / 'algorithm_comparison.csv'
    results_path = results_dir / 'mining_results.json'
    
    comparison_df = pd.read_csv(comparison_path)
    
    with open(results_path, 'r') as f:
        results_dict = json.load(f)
    
    return comparison_df, results_dict


def plot_execution_time_comparison(comparison_df: pd.DataFrame, output_dir: Path):
    """Plot execution time comparison across algorithms.
    
    Args:
        comparison_df: DataFrame with comparison results
        output_dir: Directory to save plots
    """
    plt.figure(figsize=(12, 6))
    
    plt.plot(comparison_df['min_support'], comparison_df['apriori_time (s)'], 
             marker='o', label='Apriori', linewidth=2)
    plt.plot(comparison_df['min_support'], comparison_df['fpgrowth_time (s)'], 
             marker='s', label='FP-Growth', linewidth=2)
    plt.plot(comparison_df['min_support'], comparison_df['weighted_time (s)'], 
             marker='^', label='Weighted Apriori', linewidth=2)
    
    plt.xlabel('Minimum Support', fontsize=12)
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.title('Algorithm Execution Time Comparison', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_path = output_dir / 'execution_time_comparison.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"  ✓ Saved: {output_path}")
    plt.close()


def plot_speedup_ratios(comparison_df: pd.DataFrame, output_dir: Path):
    """Plot speedup ratios relative to Weighted Apriori.
    
    Args:
        comparison_df: DataFrame with comparison results
        output_dir: Directory to save plots
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = range(len(comparison_df))
    width = 0.35
    
    ax.bar([i - width/2 for i in x], comparison_df['apriori_vs_weighted'], 
           width, label='Apriori vs Weighted', alpha=0.8)
    ax.bar([i + width/2 for i in x], comparison_df['fpgrowth_vs_weighted'], 
           width, label='FP-Growth vs Weighted', alpha=0.8)
    
    ax.axhline(y=1, color='r', linestyle='--', linewidth=2, label='Baseline (Weighted Apriori)')
    
    ax.set_xlabel('Minimum Support', fontsize=12)
    ax.set_ylabel('Speedup Ratio', fontsize=12)
    ax.set_title('Speedup Ratios Relative to Weighted Apriori', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f"{val:.2f}" for val in comparison_df['min_support']])
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    output_path = output_dir / 'speedup_ratios.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"  ✓ Saved: {output_path}")
    plt.close()


def plot_itemsets_found(comparison_df: pd.DataFrame, output_dir: Path):
    """Plot number of frequent itemsets found by each algorithm.
    
    Args:
        comparison_df: DataFrame with comparison results
        output_dir: Directory to save plots
    """
    plt.figure(figsize=(12, 6))
    
    plt.plot(comparison_df['min_support'], comparison_df['apriori_itemsets'], 
             marker='o', label='Apriori', linewidth=2)
    plt.plot(comparison_df['min_support'], comparison_df['fpgrowth_itemsets'], 
             marker='s', label='FP-Growth', linewidth=2)
    plt.plot(comparison_df['min_support'], comparison_df['weighted_itemsets'], 
             marker='^', label='Weighted Apriori', linewidth=2)
    
    plt.xlabel('Minimum Support', fontsize=12)
    plt.ylabel('Number of Frequent Itemsets', fontsize=12)
    plt.title('Frequent Itemsets Found by Algorithm', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')  # Log scale since itemsets can vary greatly
    plt.tight_layout()
    
    output_path = output_dir / 'itemsets_comparison.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"  ✓ Saved: {output_path}")
    plt.close()


def plot_heatmap_comparison(comparison_df: pd.DataFrame, output_dir: Path):
    """Create heatmap of execution times.
    
    Args:
        comparison_df: DataFrame with comparison results
        output_dir: Directory to save plots
    """
    # Prepare data for heatmap
    heatmap_data = comparison_df[['min_support', 'apriori_time (s)', 
                                   'fpgrowth_time (s)', 'weighted_time (s)']].copy()
    heatmap_data = heatmap_data.set_index('min_support')
    heatmap_data.columns = ['Apriori', 'FP-Growth', 'Weighted Apriori']
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data.T, annot=True, fmt='.4f', cmap='YlOrRd', 
                cbar_kws={'label': 'Execution Time (s)'})
    plt.title('Execution Time Heatmap', fontsize=14, fontweight='bold')
    plt.xlabel('Minimum Support', fontsize=12)
    plt.ylabel('Algorithm', fontsize=12)
    plt.tight_layout()
    
    output_path = output_dir / 'execution_time_heatmap.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"  ✓ Saved: {output_path}")
    plt.close()


def generate_all_visualizations(results_dir: Path, output_dir: Path):
    """Generate all visualization plots.
    
    Args:
        results_dir: Directory containing results files
        output_dir: Directory to save visualization outputs
    """
    print("Generating visualizations...")
    
    # Load results
    comparison_df, results_dict = load_results(results_dir)
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate plots
    plot_execution_time_comparison(comparison_df, output_dir)
    plot_speedup_ratios(comparison_df, output_dir)
    plot_itemsets_found(comparison_df, output_dir)
    plot_heatmap_comparison(comparison_df, output_dir)
    
    print(f"\n✅ All visualizations saved to: {output_dir}")


def main():
    """Main execution function."""
    project_dir = Path(__file__).resolve().parents[2]
    results_dir = project_dir / 'models'
    output_dir = project_dir / 'reports/figures'
    
    generate_all_visualizations(results_dir, output_dir)


if __name__ == '__main__':
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 6)
    
    main()
