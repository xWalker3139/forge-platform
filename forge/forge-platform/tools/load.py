"""Bounded concurrent HTTP load; run against your own local lab only."""

import argparse
import concurrent.futures
import time
import urllib.error
import urllib.request


def run(url, count, workers):
    def request(_):
        start = time.monotonic()
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                response.read()
                status = response.status
        except urllib.error.HTTPError as error:
            status = error.code
        except OSError:
            status = 0
        return status, time.monotonic() - start

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(request, range(count)))
    durations = sorted(duration for _, duration in results)
    return {
        "requests": count,
        "errors": sum(status == 0 or status >= 500 for status, _ in results),
        "p95_ms": round(durations[min(int(count * 0.95), count - 1)] * 1000, 2),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--count", type=int, default=200)
    parser.add_argument("--workers", type=int, default=10)
    args = parser.parse_args()
    if not 1 <= args.count <= 10000 or not 1 <= args.workers <= 50:
        parser.error("count 1..10000; workers 1..50")
    print(run(args.url, args.count, args.workers))
