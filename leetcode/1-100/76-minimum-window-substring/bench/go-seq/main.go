// Benchmark workload — Minimum Window Substring (LeetCode #76).
// Go single-threaded mirror of bench/minimum_window_substring.{kara,rs,c}.
// Sliding-window need/have algorithm over a fixed n=50000 sequence (alphabet
// {0,1,2,3}) built once, K=5000 iterations against a k-cycled 3-symbol target,
// folding (start, len) into a rolling hash. The O(n) window scan is the measured
// work. See ../README.md.

package main

import "fmt"

const n int64 = 50000

func minWindow(s []int64, t []int64) (int64, int64) {
	nn := int64(len(s))
	m := int64(len(t))
	if m > nn {
		return -1, 0
	}
	var need [4]int64
	var required int64 = 0
	for _, c := range t {
		if need[c] == 0 {
			required++
		}
		need[c]++
	}
	var have [4]int64
	var formed, l, bestStart, bestLen int64 = 0, 0, -1, 0
	for r := int64(0); r < nn; r++ {
		cr := s[r]
		have[cr]++
		if have[cr] == need[cr] {
			formed++
		}
		for formed == required {
			win := r - l + 1
			if bestStart == -1 || win < bestLen {
				bestStart = l
				bestLen = win
			}
			cl := s[l]
			have[cl]--
			if have[cl] < need[cl] {
				formed--
			}
			l++
		}
	}
	return bestStart, bestLen
}

func main() {
	const total int64 = 5000
	const modulus int64 = 1000000007

	s := make([]int64, n)
	for i := int64(0); i < n; i++ {
		s[i] = (i * 7) % 4
	}
	targets := [6][]int64{
		{0, 1, 2}, {1, 2, 3}, {2, 3, 0}, {3, 0, 1}, {0, 2, 3}, {1, 3, 0},
	}

	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		start, length := minWindow(s, targets[k%6])
		acc = (acc*131 + (start + 1)) % modulus
		acc = (acc*131 + length) % modulus
	}
	fmt.Println(acc)
}
