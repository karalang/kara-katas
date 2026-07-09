// Benchmark workload — Edit Distance (LeetCode #72).
// Go single-threaded mirror of bench/edit_distance.{kara,rs,c}. Faithful to the
// kata's Vec-based DP: each DP row and input string is a slice built by `append`
// (grows by doubling), matching Kāra's `Vec.new()+push` growth — NOT a fixed
// array — so the comparison measures the same growing-dynamic-array discipline.
// Rolling O(n)-space Levenshtein, K=400_000 iters over length-24 pairs.
// See ../README.md § Benchmarks.

package main

import "fmt"

func editDistance(a, b []byte, m, n int) int64 {
	var prev []int64
	for j := 0; j <= n; j++ {
		prev = append(prev, int64(j))
	}
	for i := 1; i <= m; i++ {
		cur := []int64{int64(i)}
		for j := 1; j <= n; j++ {
			if a[i-1] == b[j-1] {
				cur = append(cur, prev[j-1])
			} else {
				x := prev[j-1]
				if prev[j] < x {
					x = prev[j]
				}
				if cur[j-1] < x {
					x = cur[j-1]
				}
				cur = append(cur, 1+x)
			}
		}
		prev = cur
	}
	return prev[n]
}

func main() {
	const total int64 = 400000
	const modulus int64 = 1000000007

	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		var a, b []byte
		for p := int64(0); p < 24; p++ {
			a = append(a, byte((p*7+k)%4))
			b = append(b, byte((p*5+2*k)%4))
		}
		d := editDistance(a, b, 24, 24)
		acc = (acc*131 + d) % modulus
	}
	fmt.Println(acc)
}
