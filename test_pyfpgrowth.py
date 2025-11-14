"""
Quick test to verify pyfpgrowth integration.
"""

from src.models.mining_strategies import PyFPGrowthStrategy

# Sample transaction data
transactions = [
    {'bread', 'milk'},
    {'bread', 'diaper', 'beer', 'eggs'},
    {'milk', 'diaper', 'beer', 'cola'},
    {'bread', 'milk', 'diaper', 'beer'},
    {'bread', 'milk', 'diaper', 'cola'},
]

# Test PyFPGrowth
print("Testing PyFPGrowth Strategy...")
strategy = PyFPGrowthStrategy()

min_support = 0.4
result, exec_time = strategy.mine_frequent_itemsets(transactions, min_support)

print(f"\nMin Support: {min_support}")
print(f"Execution Time: {exec_time:.6f}s")
print(f"Frequent Itemsets Found: {len(result)}")
print("\nItemsets:")
for itemset, support in sorted(result, key=lambda x: x[1], reverse=True):
    print(f"  {itemset}: {support}")

print("\n😎 PyFPGrowth integration successful!")
