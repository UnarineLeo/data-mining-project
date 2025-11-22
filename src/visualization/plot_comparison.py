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
    
    # Use different line styles and markers to distinguish overlapping lines
    plt.plot(comparison_df['min_support'], comparison_df['apriori_time (s)'], 
             marker='o', label='Apriori', linewidth=2.5, markersize=8, 
             linestyle='-', alpha=0.8)
    plt.plot(comparison_df['min_support'], comparison_df['fpgrowth_time (s)'], 
             marker='s', label='FP-Growth', linewidth=2.5, markersize=8, 
             linestyle='--', alpha=0.8)
    plt.plot(comparison_df['min_support'], comparison_df['improved_time (s)'], 
             marker='^', label='Improved Apriori', linewidth=2.5, markersize=8, 
             linestyle='-.', alpha=0.8)
    
    plt.xlabel('Minimum Support', fontsize=12)
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.title('Algorithm Execution Time Comparison', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10, loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_path = output_dir / 'execution_time_comparison.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"  ☑ Saved: {output_path}")
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
    
    ax.bar([i - width/2 for i in x], comparison_df['apriori_vs_improved'], 
           width, label='Apriori vs Improved', alpha=0.8)
    ax.bar([i + width/2 for i in x], comparison_df['fpgrowth_vs_improved'], 
           width, label='FP-Growth vs Improved', alpha=0.8)
    
    ax.axhline(y=1, color='r', linestyle='--', linewidth=2, label='Baseline (Improved Apriori)')
    
    ax.set_xlabel('Minimum Support', fontsize=12)
    ax.set_ylabel('Speedup Ratio', fontsize=12)
    ax.set_title('Speedup Ratios Relative to Improved Apriori', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f"{val:.2f}" for val in comparison_df['min_support']])
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    output_path = output_dir / 'speedup_ratios.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"  ☑ Saved: {output_path}")
    plt.close()


def plot_itemsets_found(comparison_df: pd.DataFrame, output_dir: Path):
    """Plot number of frequent itemsets found by each algorithm.
    
    Args:
        comparison_df: DataFrame with comparison results
        output_dir: Directory to save plots
    """
    plt.figure(figsize=(12, 6))
    
    # Use different line styles and markers to distinguish overlapping lines
    plt.plot(comparison_df['min_support'], comparison_df['apriori_itemsets'], 
             marker='o', label='Apriori', linewidth=2.5, markersize=8, 
             linestyle='-', alpha=0.8)
    plt.plot(comparison_df['min_support'], comparison_df['fpgrowth_itemsets'], 
             marker='s', label='FP-Growth', linewidth=2.5, markersize=8, 
             linestyle='--', alpha=0.8)
    plt.plot(comparison_df['min_support'], comparison_df['improved_itemsets'], 
             marker='^', label='Improved Apriori', linewidth=2.5, markersize=8, 
             linestyle='-.', alpha=0.8)
    
    plt.xlabel('Minimum Support', fontsize=12)
    plt.ylabel('Number of Frequent Itemsets', fontsize=12)
    plt.title('Frequent Itemsets Found by Algorithm', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10, loc='best')
    plt.grid(True, alpha=0.3)
    plt.yscale('log')  # Log scale since itemsets can vary greatly
    plt.tight_layout()
    
    output_path = output_dir / 'itemsets_comparison.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"  ☑ Saved: {output_path}")
    plt.close()


def plot_heatmap_comparison(comparison_df: pd.DataFrame, output_dir: Path):
    """Create heatmap of execution times.
    
    Args:
        comparison_df: DataFrame with comparison results
        output_dir: Directory to save plots
    """
    # Prepare data for heatmap
    heatmap_data = comparison_df[['min_support', 'apriori_time (s)', 
                                   'fpgrowth_time (s)', 'improved_time (s)']].copy()
    heatmap_data = heatmap_data.set_index('min_support')
    heatmap_data.columns = ['Apriori', 'FP-Growth', 'Improved Apriori']
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data.T, annot=True, fmt='.4f', cmap='YlOrRd', 
                cbar_kws={'label': 'Execution Time (s)'})
    plt.title('Execution Time Heatmap', fontsize=14, fontweight='bold')
    plt.xlabel('Minimum Support', fontsize=12)
    plt.ylabel('Algorithm', fontsize=12)
    plt.tight_layout()
    
    output_path = output_dir / 'execution_time_heatmap.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"  ☑ Saved: {output_path}")
    plt.close()


def plot_itemset_size_distribution(results_dict: dict, output_dir: Path):
    """Plot distribution of itemset sizes for each algorithm.
    
    Args:
        results_dict: Dictionary with mining results including itemset_sizes
        output_dir: Directory to save plots
    """
    # Select a representative minimum support value (middle value)
    num_minsup = len(results_dict['apriori']['minsup'])
    mid_idx = num_minsup // 2
    minsup_value = results_dict['apriori']['minsup'][mid_idx]
    
    # Extract itemset size distributions for the selected minsup
    algorithms = ['apriori', 'fpgrowth', 'improved']
    algorithm_labels = ['Apriori', 'FP-Growth', 'Improved Apriori']
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle(f'Itemset Size Distribution (min_support = {minsup_value:.2f})', 
                 fontsize=14, fontweight='bold')
    
    for idx, (algo, label) in enumerate(zip(algorithms, algorithm_labels)):
        size_dist = results_dict[algo]['itemset_sizes'][mid_idx]
        
        if size_dist:
            # Convert keys to integers and sort
            sizes = sorted([int(k) for k in size_dist.keys()])
            counts = [size_dist[str(s)] for s in sizes]
            
            axes[idx].bar(sizes, counts, alpha=0.7, edgecolor='black')
            axes[idx].set_xlabel('Itemset Size', fontsize=11)
            axes[idx].set_ylabel('Count', fontsize=11)
            axes[idx].set_title(label, fontsize=12, fontweight='bold')
            axes[idx].grid(True, alpha=0.3, axis='y')
            axes[idx].set_xticks(sizes)
        else:
            axes[idx].text(0.5, 0.5, 'No data', ha='center', va='center', 
                          transform=axes[idx].transAxes, fontsize=12)
            axes[idx].set_title(label, fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    
    output_path = output_dir / 'itemset_size_distribution.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"  ☑ Saved: {output_path}")
    plt.close()
    
    # Also create a combined comparison plot
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x_offset = 0
    bar_width = 0.25
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    for idx, (algo, label, color) in enumerate(zip(algorithms, algorithm_labels, colors)):
        size_dist = results_dict[algo]['itemset_sizes'][mid_idx]
        
        if size_dist:
            # Convert keys to integers and sort
            sizes = sorted([int(k) for k in size_dist.keys()])
            counts = [size_dist[str(s)] for s in sizes]
            x_positions = [s + idx * bar_width for s in sizes]
            
            ax.bar(x_positions, counts, bar_width, label=label, 
                   alpha=0.7, edgecolor='black', color=color)
    
    ax.set_xlabel('Itemset Size', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.set_title(f'Itemset Size Distribution Comparison (min_support = {minsup_value:.2f})', 
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    output_path = output_dir / 'itemset_size_comparison.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"  ☑ Saved: {output_path}")
    plt.close()


def plot_itemset_size_trends(results_dict: dict, output_dir: Path):
    """Plot how maximum and average itemset sizes change across support thresholds.
    
    Args:
        results_dict: Dictionary with mining results including itemset_sizes
        output_dir: Directory to save plots
    """
    algorithms = ['apriori', 'fpgrowth', 'improved']
    algorithm_labels = ['Apriori', 'FP-Growth', 'Improved Apriori']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    markers = ['o', 's', '^']
    linestyles = ['-', '--', '-.']
    
    minsup_values = results_dict['apriori']['minsup']
    
    # Calculate max and average itemset sizes for each algorithm at each support
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    for idx, (algo, label, color, marker, linestyle) in enumerate(
        zip(algorithms, algorithm_labels, colors, markers, linestyles)):
        
        max_sizes = []
        avg_sizes = []
        total_itemsets = []
        size_distributions = []
        
        for size_dist in results_dict[algo]['itemset_sizes']:
            if size_dist:
                # Convert keys to integers
                sizes = [int(k) for k in size_dist.keys()]
                counts = [size_dist[str(s)] for s in sizes]
                
                max_sizes.append(max(sizes))
                
                # Calculate weighted average
                total = sum(counts)
                total_itemsets.append(total)
                weighted_sum = sum(s * c for s, c in zip(sizes, counts))
                avg_sizes.append(weighted_sum / total if total > 0 else 0)
                
                # Store full distribution for stacked area
                size_distributions.append(dict(zip(sizes, counts)))
            else:
                max_sizes.append(0)
                avg_sizes.append(0)
                total_itemsets.append(0)
                size_distributions.append({})
        
        # Plot 1: Maximum itemset size with larger markers and offset
        offset = idx * 0.002  # Slight horizontal offset for visibility
        ax1.plot([m + offset for m in minsup_values], max_sizes, 
                marker=marker, label=label, linewidth=3, markersize=10, 
                linestyle=linestyle, alpha=0.9, color=color)
        
        # Plot 2: Average itemset size with offset
        ax2.plot([m + offset for m in minsup_values], avg_sizes, 
                marker=marker, label=label, linewidth=3, markersize=10, 
                linestyle=linestyle, alpha=0.9, color=color)
        
        # Plot 3: Total itemsets (log scale)
        ax3.plot(minsup_values, total_itemsets, marker=marker, label=label, 
                linewidth=3, markersize=10, linestyle=linestyle, 
                alpha=0.9, color=color)
        
        # Plot 4: Size diversity (number of unique sizes)
        unique_sizes = [len(dist) for dist in size_distributions]
        ax4.plot(minsup_values, unique_sizes, marker=marker, label=label, 
                linewidth=3, markersize=10, linestyle=linestyle, 
                alpha=0.9, color=color)
    
    # Configure maximum size plot
    ax1.set_xlabel('Minimum Support', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Maximum Itemset Size', fontsize=12, fontweight='bold')
    ax1.set_title('Maximum Itemset Size by Algorithm', fontsize=13, fontweight='bold')
    ax1.legend(fontsize=10, loc='best')
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.invert_xaxis()
    # Add value labels at each point
    for idx, (algo, color) in enumerate(zip(algorithms, colors)):
        max_sizes_algo = []
        for size_dist in results_dict[algo]['itemset_sizes']:
            if size_dist:
                max_sizes_algo.append(max([int(k) for k in size_dist.keys()]))
            else:
                max_sizes_algo.append(0)
        for i, (x, y) in enumerate(zip(minsup_values, max_sizes_algo)):
            if i % 2 == 0:  # Label every other point to avoid crowding
                ax1.annotate(f'{y}', (x, y), textcoords="offset points", 
                           xytext=(0, 8), ha='center', fontsize=8, 
                           color=color, fontweight='bold')
    
    # Configure average size plot
    ax2.set_xlabel('Minimum Support', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Average Itemset Size', fontsize=12, fontweight='bold')
    ax2.set_title('Average Itemset Size by Algorithm', fontsize=13, fontweight='bold')
    ax2.legend(fontsize=10, loc='best')
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.invert_xaxis()
    ax2.set_ylim(bottom=0)  # Start from 0 for better comparison
    
    # Configure total itemsets plot (log scale)
    ax3.set_xlabel('Minimum Support', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Total Itemsets Found (log scale)', fontsize=12, fontweight='bold')
    ax3.set_title('Total Itemsets Discovery (Log Scale)', fontsize=13, fontweight='bold')
    ax3.legend(fontsize=10, loc='best')
    ax3.grid(True, alpha=0.3, linestyle='--')
    ax3.set_yscale('log')
    ax3.invert_xaxis()
    
    # Configure size diversity plot
    ax4.set_xlabel('Minimum Support', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Number of Unique Itemset Sizes', fontsize=12, fontweight='bold')
    ax4.set_title('Itemset Size Diversity', fontsize=13, fontweight='bold')
    ax4.legend(fontsize=10, loc='best')
    ax4.grid(True, alpha=0.3, linestyle='--')
    ax4.invert_xaxis()
    
    plt.tight_layout()
    
    output_path = output_dir / 'itemset_size_trends.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"  ☑ Saved: {output_path}")
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
    plot_itemset_size_distribution(results_dict, output_dir)
    plot_itemset_size_trends(results_dict, output_dir)
    
    print(f"\n😎 All visualizations saved to: {output_dir}")


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
