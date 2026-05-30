"""
Performance benchmarking and profiling tools.

Tools for measuring and analyzing application performance.
"""
import time
import logging
from typing import Callable, Dict, Any, List
from functools import wraps
from datetime import datetime

logger = logging.getLogger(__name__)


class Benchmark:
    """Benchmarks function performance."""
    
    def __init__(self, name: str, iterations: int = 1000):
        """Initialize benchmark.
        
        Args:
            name: Benchmark name
            iterations: Number of iterations
        """
        self.name = name
        self.iterations = iterations
        self.times = []
        self.results = {}
    
    def run(self, func: Callable, *args, **kwargs):
        """Run benchmark on function.
        
        Args:
            func: Function to benchmark
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Benchmark results dictionary
        """
        logger.info(f"Starting benchmark: {self.name}")
        
        for i in range(self.iterations):
            start_time = time.perf_counter()
            func(*args, **kwargs)
            end_time = time.perf_counter()
            self.times.append((end_time - start_time) * 1000)  # Convert to ms
        
        self.results = self.calculate_stats()
        self.log_results()
        
        return self.results
    
    def calculate_stats(self) -> Dict[str, Any]:
        """Calculate benchmark statistics.
        
        Returns:
            Statistics dictionary
        """
        if not self.times:
            return {}
        
        times = sorted(self.times)
        total = sum(times)
        count = len(times)
        
        return {
            'name': self.name,
            'iterations': count,
            'total_time_ms': total,
            'avg_time_ms': total / count,
            'min_time_ms': min(times),
            'max_time_ms': max(times),
            'median_time_ms': times[count // 2],
            'p95_time_ms': times[int(count * 0.95)],
            'p99_time_ms': times[int(count * 0.99)],
            'throughput': count / (total / 1000) if total > 0 else 0,  # ops/sec
            'timestamp': datetime.now().isoformat()
        }
    
    def log_results(self):
        """Log benchmark results."""
        r = self.results
        logger.info(
            f"Benchmark: {r['name']} - "
            f"Avg: {r['avg_time_ms']:.2f}ms, "
            f"Min: {r['min_time_ms']:.2f}ms, "
            f"Max: {r['max_time_ms']:.2f}ms, "
            f"P95: {r['p95_time_ms']:.2f}ms, "
            f"Throughput: {r['throughput']:.0f} ops/sec"
        )


class MemoryProfiler:
    """Profiles memory usage."""
    
    @staticmethod
    def get_memory_usage() -> Dict[str, Any]:
        """Get current memory usage.
        
        Returns:
            Memory statistics
        """
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            
            return {
                'rss_mb': memory_info.rss / 1024 / 1024,  # Resident set size
                'vms_mb': memory_info.vms / 1024 / 1024,  # Virtual memory size
                'percent': process.memory_percent()
            }
        except ImportError:
            logger.warning("psutil not installed. Install with: pip install psutil")
            return {}
    
    @staticmethod
    def profile_memory(f: Callable) -> Callable:
        """Decorator to profile memory usage.
        
        Args:
            f: Function to profile
            
        Returns:
            Decorated function
        """
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                import psutil
                import gc
                
                process = psutil.Process()
                gc.collect()
                memory_before = process.memory_info().rss / 1024 / 1024
                
                result = f(*args, **kwargs)
                
                gc.collect()
                memory_after = process.memory_info().rss / 1024 / 1024
                memory_delta = memory_after - memory_before
                
                logger.info(
                    f"Memory profile {f.__name__}: "
                    f"Before: {memory_before:.2f}MB, "
                    f"After: {memory_after:.2f}MB, "
                    f"Delta: {memory_delta:.2f}MB"
                )
                
                return result
            except ImportError:
                logger.warning("psutil not installed for memory profiling")
                return f(*args, **kwargs)
        
        return wrapper


class CPUProfiler:
    """Profiles CPU usage."""
    
    @staticmethod
    def profile_cpu(f: Callable) -> Callable:
        """Decorator to profile CPU usage.
        
        Args:
            f: Function to profile
            
        Returns:
            Decorated function
        """
        @wraps(f)
        def wrapper(*args, **kwargs):
            import cProfile
            import pstats
            import io
            
            pr = cProfile.Profile()
            pr.enable()
            
            result = f(*args, **kwargs)
            
            pr.disable()
            
            s = io.StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
            ps.print_stats(10)  # Print top 10 functions
            
            logger.debug(f"CPU Profile for {f.__name__}:\n{s.getvalue()}")
            
            return result
        
        return wrapper


class PerformanceTester:
    """Runs comprehensive performance tests."""
    
    def __init__(self):
        """Initialize performance tester."""
        self.benchmarks = []
    
    def add_benchmark(self, name: str, func: Callable, iterations: int = 1000):
        """Add benchmark to test suite.
        
        Args:
            name: Benchmark name
            func: Function to benchmark
            iterations: Number of iterations
        """
        benchmark = Benchmark(name, iterations)
        benchmark.run(func)
        self.benchmarks.append(benchmark)
    
    def run_suite(self) -> List[Dict[str, Any]]:
        """Run all benchmarks.
        
        Returns:
            List of results
        """
        logger.info(f"Running performance test suite with {len(self.benchmarks)} tests")
        
        results = []
        for benchmark in self.benchmarks:
            results.append(benchmark.results)
        
        return results
    
    def generate_report(self) -> str:
        """Generate performance report.
        
        Returns:
            Formatted report string
        """
        lines = ["Performance Test Report", "=" * 50]
        
        for benchmark in self.benchmarks:
            r = benchmark.results
            lines.append(f"\nBenchmark: {r['name']}")
            lines.append(f"  Iterations: {r['iterations']}")
            lines.append(f"  Average: {r['avg_time_ms']:.2f}ms")
            lines.append(f"  Min: {r['min_time_ms']:.2f}ms")
            lines.append(f"  Max: {r['max_time_ms']:.2f}ms")
            lines.append(f"  P95: {r['p95_time_ms']:.2f}ms")
            lines.append(f"  Throughput: {r['throughput']:.0f} ops/sec")
        
        return "\n".join(lines)
