// Benchmark workload — Climbing Stairs (LeetCode #70).
// Go single-threaded mirror of bench/climbing_stairs.{kara,rs,c}. The ★'s
// two-counter Fibonacci recurrence run K=30_000_000 times over a sweep of
// n = 1 + k%45, folding each result into a rolling polynomial hash. No
// allocation — a pure integer-add / branch benchmark. See ../README.md § Benchmarks.

package main

import "fmt"

func climb(n int64) int64 {
	if n <= 2 {
		return n
	}
	var a, b int64 = 1, 2
	for i := int64(3); i <= n; i++ {
		next := a + b
		a = b
		b = next
	}
	return b
}

func main() {
	const total int64 = 30000000
	const modulus int64 = 1000000007
	const span int64 = 45

	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		n := 1 + (k % span)
		acc = (acc*131 + climb(n)) % modulus
	}
	fmt.Println(acc)
}
