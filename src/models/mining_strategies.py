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
    """FP-Growth algorithm using mlxtend."""
    
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
        return "FP-Growth"


class WeightedAprioriStrategy(MiningStrategy):
    """Weighted Apriori algorithm with optimized database scans."""
    
    def __init__(self):
        self.database = None
        self.wminsup = None
        self.num_transactions = 0
    
    def mine_frequent_itemsets(self, transactions_list: List[Set], min_support: float) -> Tuple[List[Tuple], float]:
        """Mine frequent itemsets using Weighted Apriori.
        
        Args:
            transactions_list: List of transaction sets
            min_support: Minimum support threshold (0-1)
            
        Returns:
            Tuple of (frequent_itemsets list, execution_time)
        """
        self.database = transactions_list
        self.num_transactions = len(transactions_list)
        self.wminsup = int(min_support * self.num_transactions)
        
        start_time = time.time()
        frequent_itemsets = self._locate_frequent_k_itemset()
        execution_time = time.time() - start_time
        
        # Convert to list format: [(itemset, support_count), ...]
        result = []
        for k, itemsets in frequent_itemsets.items():
            for itemset, sup_trans in itemsets.items():
                result.append((set(itemset), len(sup_trans)))
        
        return result, execution_time
    
    def get_algorithm_name(self) -> str:
        return "Weighted Apriori"
    
    def _generate_c1(self) -> Dict[frozenset, Set[int]]:
        """Generate candidate 1-itemsets."""
        c1 = defaultdict(set)
        for tid, transaction in enumerate(self.database):
            for item in transaction:
                c1[frozenset([item])].add(tid)
        return c1
    
    def _locate_frequent_1_itemset(self, c1: Dict) -> Dict:
        """Filter frequent 1-itemsets based on minimum support."""
        l1 = {}
        for itemset, sup_trans in c1.items():
            count = len(sup_trans)
            if count >= self.wminsup:
                l1[itemset] = sup_trans
        return l1
    
    def _apriori_gen(self, lk_prev: Dict) -> Dict:
        """Generate candidate k-itemsets from frequent (k-1)-itemsets."""
        ck = {}
        itemsets = list(lk_prev.keys())
        
        for i in range(len(itemsets)):
            for j in range(i + 1, len(itemsets)):
                g1 = sorted(itemsets[i])
                g2 = sorted(itemsets[j])
                
                # Join step: merge if first k-2 items are identical
                if g1[:-1] == g2[:-1] and g1[-1] < g2[-1]:
                    c = frozenset(g1 + [g2[-1]])
                    
                    # Prune step: check if all subsets are frequent
                    if self._has_infrequent_subset(c, lk_prev):
                        continue
                    
                    ck[c] = set()
        
        return ck
    
    def _has_infrequent_subset(self, candidate: frozenset, lk_prev: Dict) -> bool:
        """Check if candidate has any infrequent subset."""
        k = len(candidate)
        for subset in combinations(candidate, k - 1):
            if frozenset(subset) not in lk_prev:
                return True
        return False
    
    def _locate_frequent_k_itemset(self) -> Dict[int, Dict]:
        """Main algorithm to find all frequent itemsets."""
        # Generate frequent 1-itemsets
        c1 = self._generate_c1()
        l1 = self._locate_frequent_1_itemset(c1)
        all_frequent = {1: l1}
        
        lk_prev = l1
        k = 2
        
        # Iteratively generate frequent k-itemsets
        while lk_prev:
            ck = self._apriori_gen(lk_prev)
            if not ck:
                break
            
            # Calculate support using intersection of transaction sets
            for c in ck:
                c_sup_trans = None
                for subset in combinations(c, k - 1):
                    subset_frozen = frozenset(subset)
                    s_sup_trans = lk_prev.get(subset_frozen, set())
                    
                    if c_sup_trans is None:
                        c_sup_trans = s_sup_trans.copy()
                    else:
                        c_sup_trans = c_sup_trans.intersection(s_sup_trans)
                
                ck[c] = c_sup_trans if c_sup_trans else set()
            
            # Filter by minimum support
            lk = {}
            for c, sup_trans in ck.items():
                count = len(sup_trans)
                if count >= self.wminsup:
                    lk[c] = sup_trans
            
            if lk:
                all_frequent[k] = lk
                lk_prev = lk
                k += 1
            else:
                break
        
        return all_frequent


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
