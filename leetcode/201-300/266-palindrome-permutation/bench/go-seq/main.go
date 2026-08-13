// Benchmark workload for LeetCode #266 — Palindrome Permutation (Go mirror).
// Mirrors pal_perm.kara algorithm-for-algorithm.
package main

import "fmt"

func main() {
	var n int64 = 200000
	var rounds int64 = 4000
	var span int64 = 1000
	width := n - span

	data := make([]int64, n)
	var state int64 = 266266
	for z := int64(0); z < n; z++ {
		state = (state*1103515245 + 12345) & 2147483647
		data[z] = 97 + (state/65536)%26
	}

	counts := make([]int64, 256)

	var sink int64 = 0
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < 256; c++ {
			counts[c] = 0
		}

		start := (r * 7919) % span
		stop := start + width
		for i := start; i < stop; i++ {
			b := data[i]
			counts[b]++
		}

		var odd int64 = 0
		for k := 0; k < 256; k++ {
			if counts[k]%2 == 1 {
				odd++
			}
		}
		var verdict int64 = 0
		if odd <= 1 {
			verdict = 1
		}
		sink = (sink*131 + odd*7 + verdict) % 1000000007
	}

	fmt.Println(sink)
}
