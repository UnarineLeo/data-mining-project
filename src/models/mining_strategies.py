"""
Strategy pattern implementation for association rule mining algorithms.

This module provides a common interface for different mining algorithms
(Apriori, FP-Growth, Weighted Apriori) to enable easy comparison and switching.
"""

from abc import ABC, abstractmethod
from itertools import combinations
from collections import defaultdict
import time
import pandas as pd
from typing import List, Set, Dict, Tuple, Any


class MiningStrategy(ABC):
    """Abstract base class for association rule mining strategies."""
    
    @abstractmethod
    def mine_frequent_itemsets(self, data, min_support: float) -> Tuple[Any, float]:
        """Mine frequent itemsets from data.
        
        Args:
            data: Input data (format depends on algorithm)
            min_support: Minimum support threshold
            
        Returns:
            Tuple of (frequent_itemsets, execution_time)
        """
        pass
    
    @abstractmethod
    def get_algorithm_name(self) -> str:
        """Return the name of the algorithm."""
        pass


class AprioriStrategy(MiningStrategy):
    """Standard Apriori algorithm using mlxtend."""
    
    def mine_frequent_itemsets(self, df_encoded: pd.DataFrame, min_support: float) -> Tuple[pd.DataFrame, float]:
        """Mine frequent itemsets using Apriori algorithm.
        
        Args:
            df_encoded: One-hot encoded transaction DataFrame
            min_support: Minimum support threshold (0-1)
            
        Returns:
            Tuple of (frequent_itemsets DataFrame, execution_time)
        """
        from mlxtend.frequent_patterns import apriori
        
        start_time = time.time()
        frequent_itemsets = apriori(df_encoded, min_support=min_support, use_colnames=True)
        execution_time = time.time() - start_time
        
        return frequent_itemsets, execution_time
    
    def get_algorithm_name(self) -> str:
        return "Apriori"


class FPGrowthStrategy(MiningStrategy):
    """FP-Growth algorithm using pyfpgrowth library."""
    
    def mine_frequent_itemsets(self, transactions_list: List[Set], min_support: float) -> Tuple[List[Tuple], float]:
        """Mine frequent itemsets using FP-Growth algorithm.
        
        Args:
            transactions_list: List of transaction sets
            min_support: Minimum support threshold (0-1)
            
        Returns:
            Tuple of (frequent_itemsets list, execution_time)
        """
        try:
            import pyfpgrowth
        except ImportError:
            raise ImportError("pyfpgrowth is not installed. Install with: pip install pyfpgrowth")
        
        # Convert sets to lists for pyfpgrowth
        transactions_as_lists = [list(t) for t in transactions_list]
        min_support_count = int(min_support * len(transactions_list))
        
        start_time = time.time()
        patterns = pyfpgrowth.find_frequent_patterns(transactions_as_lists, min_support_count)
        execution_time = time.time() - start_time
        
        # Convert to standard format: [(itemset, support_count), ...]
        result = [(set(itemset), support) for itemset, support in patterns.items()]
        
        return result, execution_time
    
    def get_algorithm_name(self) -> str:
        return "FP-Growth"


class FPGrowthMLXtendStrategy(MiningStrategy):
    """FP-Growth algorithm using mlxtend (slower, kept for comparison)."""
    
    def mine_frequent_itemsets(self, df_encoded: pd.DataFrame, min_support: float) -> Tuple[pd.DataFrame, float]:
        """Mine frequent itemsets using FP-Growth algorithm.
        
        Args:
            df_encoded: One-hot encoded transaction DataFrame
            min_support: Minimum support threshold (0-1)
            
        Returns:
            Tuple of (frequent_itemsets DataFrame, execution_time)
        """
        from mlxtend.frequent_patterns import fpgrowth
        
        start_time = time.time()
        frequent_itemsets = fpgrowth(df_encoded, min_support=min_support, use_colnames=True)
        execution_time = time.time() - start_time
        
        return frequent_itemsets, execution_time
    
    def get_algorithm_name(self) -> str:
        return "FP-Growth (mlxtend)"


class PyFPGrowthStrategy(MiningStrategy):
    """Alias for FPGrowthStrategy - kept for backwards compatibility."""
    
    def __init__(self):
        self._strategy = FPGrowthStrategy()
    
    def mine_frequent_itemsets(self, transactions_list: List[Set], min_support: float) -> Tuple[List[Tuple], float]:
        return self._strategy.mine_frequent_itemsets(transactions_list, min_support)
    
    def get_algorithm_name(self) -> str:
        return self._strategy.get_algorithm_name()


class ImprovedAprioriStrategy(MiningStrategy):
    """Improved Apriori (2-Phase) implementation using tidlist / vertical format."""
    
    def mine_frequent_itemsets(self, transactions_list: List[Set], min_support: float) -> Tuple[List[Tuple], float]:
        """Mine frequent itemsets using Improved Apriori (2-phase tidlist).
        
        Args:
            transactions_list: List of transaction sets
            min_support: Minimum support threshold (0-1)
            
        Returns:
            Tuple of (frequent_itemsets list, execution_time)
        """
        start_time = time.time()
        
        # Convert to list of sets
        transactions = [set(tx) for tx in transactions_list]
        n_transactions = len(transactions)
        min_support_count = max(1, int(min_support * n_transactions))
        
        # Phase 1: Build tidlists (single DB scan)
        transactions_map, item_tid = self._build_tidlists(transactions)
        
        # Compute L1
        L = []  # list of dicts: L[k-1] contains frequent k-itemsets
        L1 = {}
        for item, tids in item_tid.items():
            sup_count = len(tids)
            if sup_count >= min_support_count:
                L1[frozenset([item])] = (tids, sup_count)
        L.append(L1)
        
        # Result list
        frequent_itemsets = []
        # Store L1 in result
        for itemset, (tids, sc) in L1.items():
            frequent_itemsets.append((set(itemset), sc))
        
        # Generate higher-level itemsets
        k = 2
        while True:
            prev_L = L[-1]
            if len(prev_L) < 2:
                break  # can't join to make larger sets
            
            # Candidate generation: join step
            prev_itemsets = sorted(prev_L.keys(), key=lambda fs: tuple(sorted(fs)))
            Ck = {}
            
            # Join pairs of previous (k-1)-itemsets
            for i in range(len(prev_itemsets)):
                for j in range(i+1, len(prev_itemsets)):
                    a = prev_itemsets[i]
                    b = prev_itemsets[j]
                    # Attempt join
                    union = a | b
                    if len(union) != k:
                        continue
                    
                    # Intersect tidlists of a and b
                    tids_a = prev_L[a][0]
                    tids_b = prev_L[b][0]
                    inter_tids = tids_a & tids_b
                    sup_count = len(inter_tids)
                    
                    if sup_count >= min_support_count:
                        Ck[frozenset(union)] = (inter_tids, sup_count)
            
            if not Ck:
                break
            
            # Add to L and to result
            L.append(Ck)
            for itemset, (tids, sc) in Ck.items():
                frequent_itemsets.append((set(itemset), sc))
            k += 1
        
        execution_time = time.time() - start_time
        return frequent_itemsets, execution_time
    
    def _build_tidlists(self, transactions):
        """
        Phase 1: Single pass over transactions to build:
          - transactions_map: {tid: set(items)}
          - item_tid: {item: set(tids)}
        """
        transactions_map = {}
        item_tid = defaultdict(set)
        
        for tid, tx in enumerate(transactions):
            itemset = set(tx)
            transactions_map[tid] = itemset
            for item in itemset:
                item_tid[item].add(tid)
        
        return transactions_map, item_tid
    
    def get_algorithm_name(self) -> str:
        return "Improved Apriori"


# Alias for backward compatibility
class WeightedAprioriStrategy(ImprovedAprioriStrategy):
    """Alias for ImprovedAprioriStrategy - kept for backward compatibility."""
    pass


class MiningContext:
    """Context class that uses a mining strategy."""
    
    def __init__(self, strategy: MiningStrategy):
        self._strategy = strategy
    
    @property
    def strategy(self) -> MiningStrategy:
        return self._strategy
    
    @strategy.setter
    def strategy(self, strategy: MiningStrategy) -> None:
        self._strategy = strategy
    
    def execute_mining(self, data: Any, min_support: float) -> Tuple[Any, float]:
        """Execute mining using the current strategy.
        
        Args:
            data: Input data
            min_support: Minimum support threshold
            
        Returns:
            Tuple of (frequent_itemsets, execution_time)
        """
        return self._strategy.mine_frequent_itemsets(data, min_support)
    
    def get_algorithm_name(self) -> str:
        """Get the name of the current algorithm."""
        return self._strategy.get_algorithm_name()
