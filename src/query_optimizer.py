"""
Database query optimization module.

Provides utilities for optimizing database queries and indexing.
"""
import logging
import time
from typing import List, Dict, Any, Callable, Optional
from functools import wraps

logger = logging.getLogger(__name__)


class QueryOptimizer:
    """Optimizes database queries."""
    
    # Query execution times for analysis
    QUERY_TIMES = {
        'fast': 0.1,  # < 100ms
        'normal': 0.5,  # < 500ms
        'slow': 1.0,  # < 1s
        'very_slow': float('inf')  # > 1s
    }
    
    @staticmethod
    def analyze_query_performance(query_time: float) -> str:
        """Analyze query performance.
        
        Args:
            query_time: Query execution time in seconds
            
        Returns:
            Performance classification
        """
        for classification, threshold in QueryOptimizer.QUERY_TIMES.items():
            if query_time <= threshold:
                return classification
        return 'very_slow'
    
    @staticmethod
    def log_slow_query(query: str, execution_time: float, threshold: float = 0.5):
        """Log slow query execution.
        
        Args:
            query: SQL query
            execution_time: Execution time in seconds
            threshold: Slow query threshold in seconds
        """
        if execution_time > threshold:
            logger.warning(
                f"Slow query detected ({execution_time:.2f}s): {query[:100]}..."
            )


class IndexStrategy:
    """Database indexing strategy."""
    
    # Common indexes for medical chatbot
    RECOMMENDED_INDEXES = {
        'users': ['id', 'email', 'created_at'],
        'conversations': ['user_id', 'created_at', 'updated_at'],
        'messages': ['conversation_id', 'created_at'],
        'embeddings': ['document_id', 'created_at']
    }
    
    @staticmethod
    def get_recommended_indexes(table: str) -> List[str]:
        """Get recommended indexes for table.
        
        Args:
            table: Table name
            
        Returns:
            List of recommended column names to index
        """
        return IndexStrategy.RECOMMENDED_INDEXES.get(table, [])
    
    @staticmethod
    def suggest_composite_indexes() -> Dict[str, List[str]]:
        """Suggest composite indexes for better performance.
        
        Returns:
            Dictionary of table -> composite index columns
        """
        return {
            'conversations': ['user_id', 'created_at'],
            'messages': ['conversation_id', 'created_at'],
            'embeddings': ['document_id', 'created_at']
        }


class QueryCache:
    """Caches frequently executed queries."""
    
    def __init__(self, ttl_seconds: int = 300):
        """Initialize query cache.
        
        Args:
            ttl_seconds: Time to live for cache entries
        """
        self.cache = {}
        self.ttl_seconds = ttl_seconds
    
    def get(self, query: str) -> Optional[Any]:
        """Get cached query result.
        
        Args:
            query: Query string
            
        Returns:
            Cached result or None
        """
        if query in self.cache:
            result, timestamp = self.cache[query]
            age = time.time() - timestamp
            
            if age < self.ttl_seconds:
                logger.debug(f"Cache hit for query: {query[:50]}...")
                return result
            else:
                del self.cache[query]
        
        return None
    
    def set(self, query: str, result: Any):
        """Cache query result.
        
        Args:
            query: Query string
            result: Query result
        """
        self.cache[query] = (result, time.time())
        logger.debug(f"Cached query result: {query[:50]}...")
    
    def clear(self):
        """Clear all cached queries."""
        self.cache.clear()
        logger.info("Query cache cleared")


# Global query cache instance
query_cache = QueryCache(ttl_seconds=300)


def optimize_query(f: Callable) -> Callable:
    """Decorator to optimize and log query execution.
    
    Args:
        f: Function to decorate
        
    Returns:
        Decorated function
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = f(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Log performance
            performance = QueryOptimizer.analyze_query_performance(execution_time)
            logger.info(
                f"Query executed in {execution_time:.2f}s ({performance})"
            )
            
            # Log if slow
            if execution_time > 0.5:
                QueryOptimizer.log_slow_query(
                    f.__name__,
                    execution_time
                )
            
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Query failed after {execution_time:.2f}s: {str(e)}")
            raise
    
    return wrapper


class QueryBuilder:
    """Helper for building optimized queries."""
    
    @staticmethod
    def build_select_query(
        table: str,
        columns: List[str] = None,
        where: Dict[str, Any] = None,
        order_by: str = None,
        limit: int = None
    ) -> str:
        """Build SELECT query.
        
        Args:
            table: Table name
            columns: Columns to select (None = all)
            where: WHERE conditions
            order_by: ORDER BY clause
            limit: LIMIT clause
            
        Returns:
            SQL query string
        """
        cols = ', '.join(columns) if columns else '*'
        query = f"SELECT {cols} FROM {table}"
        
        if where:
            conditions = [f"{k}={v}" for k, v in where.items()]
            query += " WHERE " + " AND ".join(conditions)
        
        if order_by:
            query += f" ORDER BY {order_by}"
        
        if limit:
            query += f" LIMIT {limit}"
        
        return query
    
    @staticmethod
    def suggest_optimization(query: str) -> List[str]:
        """Suggest optimizations for query.
        
        Args:
            query: SQL query
            
        Returns:
            List of optimization suggestions
        """
        suggestions = []
        
        query_upper = query.upper()
        
        # Check for SELECT *
        if 'SELECT *' in query_upper:
            suggestions.append("Avoid SELECT * - specify needed columns")
        
        # Check for missing WHERE
        if 'FROM' in query_upper and 'WHERE' not in query_upper:
            suggestions.append("Consider adding WHERE clause to reduce rows")
        
        # Check for OR conditions
        if ' OR ' in query_upper:
            suggestions.append("Consider using IN clause instead of multiple OR")
        
        # Check for LIKE with leading %
        if "LIKE '%'" in query_upper:
            suggestions.append("Leading % in LIKE can prevent index usage")
        
        return suggestions
