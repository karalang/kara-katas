// LeetCode 204 — Go goroutine-parallel mirror. Spawns
// `runtime.NumCPU()` workers, each scanning a chunk of `[0, n)`
// into a private `[]int64`, then a final merge into a flat result.
// Same shape Kāra's `#[par_unordered]` and Rust's `rayon` use:
// per-worker partials, no shared accumulator during the loop, final
// concat at the end. Same sink as the other par-lane mirrors for
// N = 10_000_000.
package main

import (
	"fmt"
	"runtime"
	"sync"
)

func isPrime(n int64) bool {
	if n < 2 {
		return false
	}
	if n == 2 {
		return true
	}
	if n%2 == 0 {
		return false
	}
	for i := int64(3); i*i <= n; i += 2 {
		if n%i == 0 {
			return false
		}
	}
	return true
}

func main() {
	const n int64 = 10_000_000
	workers := runtime.NumCPU()
	chunk := n / int64(workers)

	partials := make([][]int64, workers)
	var wg sync.WaitGroup
	wg.Add(workers)

	for w := 0; w < workers; w++ {
		go func(w int) {
			defer wg.Done()
			start := int64(w) * chunk
			end := start + chunk
			if w == workers-1 {
				end = n
			}
			local := make([]int64, 0)
			for k := start; k < end; k++ {
				if isPrime(k) {
					local = append(local, k)
				}
			}
			partials[w] = local
		}(w)
	}
	wg.Wait()

	// Merge: pre-size the destination buffer, then concat.
	totalLen := 0
	for _, p := range partials {
		totalLen += len(p)
	}
	primes := make([]int64, 0, totalLen)
	for _, p := range partials {
		primes = append(primes, p...)
	}

	var sum int64
	for _, p := range primes {
		sum += p
	}
	fmt.Println(len(primes))
	fmt.Println(sum)
}
