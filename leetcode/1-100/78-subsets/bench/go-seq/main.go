// Benchmark workload — Subsets (LeetCode #78).
// Go single-threaded mirror of bench/subsets.{kara,rs,c}. Emit-at-every-node
// backtracking that ENUMERATES the power set of [1..16] (2^16 subsets) and folds each
// node's path into a threaded accumulator (no storage), K=300 iterations seeded by
// the iteration index. The path is a small stack buffer indexed by depth. See
// ../README.md.

package main

import "fmt"

func enumerate(nums []int64, n, start int64, path []int64, depth, acc int64) int64 {
	a := acc
	a = (a*131 + (depth + 1)) % 1000000007
	for p := int64(0); p < depth; p++ {
		a = (a*131 + path[p]) % 1000000007
	}
	for i := start; i < n; i++ {
		path[depth] = nums[i]
		a = enumerate(nums, n, i+1, path, depth+1, a)
	}
	return a
}

func main() {
	const n, total, modulus int64 = 16, 300, 1000000007
	nums := make([]int64, n)
	for i := int64(0); i < n; i++ {
		nums[i] = i + 1
	}
	path := make([]int64, 64)
	var sum int64 = 0
	for iter := int64(0); iter < total; iter++ {
		r := enumerate(nums, n, 0, path, 0, iter)
		sum = (sum + r) % modulus
	}
	fmt.Println(sum)
}
