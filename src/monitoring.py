"""
Monitoring and metrics collection module.

Collects and tracks performance metrics for the chatbot application.
"""
import time
import logging
from datetime import datetime
from typing import Dict, Any, List
from functools import wraps

logger = logging.getLogger(__name__)


class MetricsCollector:
    """Collects application metrics."""
    
    def __init__(self):
        """Initialize metrics collector."""
        self.metrics = {
            'requests': 0,
            'errors': 0,
            'total_response_time': 0.0,
            'avg_response_time': 0.0,
            'cache_hits': 0,
            'cache_misses': 0,
            'api_calls': {},
            'endpoint_stats': {}
        }
    
    def record_request(self, endpoint: str, response_time: float, status_code: int):
        """Record request metrics.
        
        Args:
            endpoint: API endpoint
            response_time: Response time in seconds
            status_code: HTTP status code
        """
        self.metrics['requests'] += 1
        self.metrics['total_response_time'] += response_time
        self.metrics['avg_response_time'] = (
            self.metrics['total_response_time'] / self.metrics['requests']
        )
        
        if status_code >= 400:
            self.metrics['errors'] += 1
        
        # Record endpoint-specific stats
        if endpoint not in self.metrics['endpoint_stats']:
            self.metrics['endpoint_stats'][endpoint] = {
                'count': 0,
                'total_time': 0.0,
                'avg_time': 0.0,
                'errors': 0
            }
        
        stats = self.metrics['endpoint_stats'][endpoint]
        stats['count'] += 1
        stats['total_time'] += response_time
        stats['avg_time'] = stats['total_time'] / stats['count']
        
        if status_code >= 400:
            stats['errors'] += 1
        
        logger.debug(
            f"Recorded metrics - Endpoint: {endpoint}, "
            f"Time: {response_time:.2f}s, Status: {status_code}"
        )
    
    def record_cache_hit(self):
        """Record cache hit."""
        self.metrics['cache_hits'] += 1
    
    def record_cache_miss(self):
        """Record cache miss."""
        self.metrics['cache_misses'] += 1
    
    def record_api_call(self, api_name: str, response_time: float, success: bool):
        """Record external API call.
        
        Args:
            api_name: Name of external API
            response_time: Response time in seconds
            success: Whether call was successful
        """
        if api_name not in self.metrics['api_calls']:
            self.metrics['api_calls'][api_name] = {
                'calls': 0,
                'successes': 0,
                'failures': 0,
                'total_time': 0.0,
                'avg_time': 0.0
            }
        
        stats = self.metrics['api_calls'][api_name]
        stats['calls'] += 1
        stats['total_time'] += response_time
        stats['avg_time'] = stats['total_time'] / stats['calls']
        
        if success:
            stats['successes'] += 1
        else:
            stats['failures'] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics.
        
        Returns:
            Dictionary of metrics
        """
        cache_total = self.metrics['cache_hits'] + self.metrics['cache_misses']
        cache_hit_rate = 0
        if cache_total > 0:
            cache_hit_rate = (self.metrics['cache_hits'] / cache_total) * 100
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_requests': self.metrics['requests'],
            'total_errors': self.metrics['errors'],
            'error_rate': (
                (self.metrics['errors'] / self.metrics['requests'] * 100)
                if self.metrics['requests'] > 0 else 0
            ),
            'avg_response_time': f"{self.metrics['avg_response_time']:.2f}s",
            'cache_hits': self.metrics['cache_hits'],
            'cache_misses': self.metrics['cache_misses'],
            'cache_hit_rate': f"{cache_hit_rate:.2f}%",
            'endpoint_stats': self.metrics['endpoint_stats'],
            'api_calls': self.metrics['api_calls']
        }
    
    def reset(self):
        """Reset metrics."""
        self.metrics = {
            'requests': 0,
            'errors': 0,
            'total_response_time': 0.0,
            'avg_response_time': 0.0,
            'cache_hits': 0,
            'cache_misses': 0,
            'api_calls': {},
            'endpoint_stats': {}
        }
        logger.info("Metrics reset")


# Global metrics collector instance
metrics_collector = MetricsCollector()


def track_metrics(f):
    """Decorator to track metrics for endpoints.
    
    Args:
        f: Function to decorate
        
    Returns:
        Decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = f(*args, **kwargs)
            
            # Extract status code from response
            if isinstance(result, tuple):
                response, status_code = result
            else:
                status_code = 200
            
            response_time = time.time() - start_time
            metrics_collector.record_request(
                f.__name__,
                response_time,
                status_code
            )
            
            return result
        except Exception as e:
            response_time = time.time() - start_time
            metrics_collector.record_request(
                f.__name__,
                response_time,
                500
            )
            raise
    
    return decorated_function


class PerformanceMonitor:
    """Monitors application performance."""
    
    THRESHOLDS = {
        'response_time': 1.0,  # seconds
        'error_rate': 5.0,  # percentage
        'cache_hit_rate': 50.0  # percentage
    }
    
    @staticmethod
    def check_performance() -> List[str]:
        """Check performance against thresholds.
        
        Returns:
            List of alerts if thresholds exceeded
        """
        alerts = []
        metrics = metrics_collector.get_metrics()
        
        # Check response time
        avg_time = float(metrics['avg_response_time'].rstrip('s'))
        if avg_time > PerformanceMonitor.THRESHOLDS['response_time']:
            alerts.append(
                f"Average response time {avg_time:.2f}s exceeds "
                f"threshold {PerformanceMonitor.THRESHOLDS['response_time']}s"
            )
        
        # Check error rate
        if metrics['error_rate'] > PerformanceMonitor.THRESHOLDS['error_rate']:
            alerts.append(
                f"Error rate {metrics['error_rate']:.2f}% exceeds "
                f"threshold {PerformanceMonitor.THRESHOLDS['error_rate']}%"
            )
        
        if alerts:
            logger.warning("Performance thresholds exceeded: " + "; ".join(alerts))
        
        return alerts
