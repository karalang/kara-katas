// Benchmark workload — Combinations (LeetCode #77).
// Go single-threaded mirror of bench/combinations.{kara,rs,c}. Start-indexed pruned
// backtracking that ENUMERATES all C(16,8)=12870 combinations and folds each leaf's
// values into a threaded accumulator (no storage), K=1500 iterations seeded by the
// iteration index. The path is a small stack buffer indexed by depth. See ../README.md.

package main

import "fmt"

func enumerate(n, k, start int64, path []int64, depth, acc int64) int64 {
	if depth == k {
		a := acc
		for j := int64(0); j < k; j++ {
			a = (a*131 + path[j]) % 1000000007
		}
		return a
	}
	need := k - depth
	limit := n - need + 1
	a := acc
	for i := start; i <= limit; i++ {
		path[depth] = i
		a = enumerate(n, k, i+1, path, depth+1, a)
	}
	return a
}

func main() {
	const n, k, total, modulus int64 = 16, 8, 1500, 1000000007
	path := make([]int64, 64)
	var sum int64 = 0
	for iter := int64(0); iter < total; iter++ {
		r := enumerate(n, k, 1, path, 0, iter)
		sum = (sum + r) % modulus
	}
	fmt.Println(sum)
}
