"""
Database connection pooling configuration.

This module manages connection pooling for improved database performance.
"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ConnectionPool:
    """Database connection pool manager."""
    
    def __init__(self, pool_size=10, max_overflow=20):
        """Initialize connection pool.
        
        Args:
            pool_size: Number of connections to maintain
            max_overflow: Maximum overflow connections
        """
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.connections = []
        self.active_connections = 0
        logger.info(f"Initialized connection pool with size {pool_size}")
    
    def get_connection(self) -> Optional[object]:
        """Get a connection from the pool.
        
        Returns:
            Connection object or None if unavailable
        """
        if self.connections:
            conn = self.connections.pop()
            self.active_connections += 1
            logger.debug(f"Got connection from pool. Active: {self.active_connections}")
            return conn
        
        if self.active_connections < self.pool_size + self.max_overflow:
            self.active_connections += 1
            logger.debug(f"Created new connection. Active: {self.active_connections}")
            return {"connection": True}  # Placeholder
        
        logger.warning("Connection pool exhausted")
        return None
    
    def return_connection(self, conn):
        """Return connection to pool.
        
        Args:
            conn: Connection object to return
        """
        if conn:
            self.connections.append(conn)
            self.active_connections -= 1
            logger.debug(f"Returned connection to pool. Active: {self.active_connections}")
    
    def get_stats(self):
        """Get pool statistics.
        
        Returns:
            dict: Pool statistics
        """
        return {
            "pool_size": self.pool_size,
            "available": len(self.connections),
            "active": self.active_connections,
            "max_overflow": self.max_overflow
        }


class Config:
    """Database configuration."""
    
    # Connection pool settings
    POOL_SIZE = 10
    POOL_MAX_OVERFLOW = 20
    POOL_TIMEOUT = 30
    POOL_RECYCLE = 3600  # Recycle connections every hour
    
    # Connection settings
    ECHO_POOL = False  # Log connection pool activity
    POOL_PRE_PING = True  # Test connection before using
    
    @classmethod
    def get_pool_config(cls):
        """Get complete pool configuration.
        
        Returns:
            dict: Pool configuration
        """
        return {
            "pool_size": cls.POOL_SIZE,
            "max_overflow": cls.POOL_MAX_OVERFLOW,
            "pool_timeout": cls.POOL_TIMEOUT,
            "pool_recycle": cls.POOL_RECYCLE,
            "echo_pool": cls.ECHO_POOL,
            "pool_pre_ping": cls.POOL_PRE_PING
        }


# Global connection pool instance
connection_pool = ConnectionPool(
    pool_size=Config.POOL_SIZE,
    max_overflow=Config.POOL_MAX_OVERFLOW
)
