// Benchmark workload — Scramble String (LeetCode #87), SEQ lane.
// Go mirror of ../scramble_string.kara. Each iteration builds a length-12 string and a
// coprime-step permutation of it, runs the O(n^4) top-down memoized scramble, and folds
// the filled memo state into a work-sensitive checksum added to an associative sum.
// Same len/K. The go-par/ sibling parallelises with goroutines.
package main

import "fmt"

func scramble(s1 []byte, i1 int64, s2 []byte, i2, length int64, memo []int64, n int64) bool {
	if length == 0 {
		return true
	}
	key := (i1*n + i2) * (n + 1) + length
	if memo[key] != -1 {
		return memo[key] == 1
	}
	equal := true
	for k := int64(0); k < length; k++ {
		if s1[i1+k] != s2[i2+k] {
			equal = false
			break
		}
	}
	if equal {
		memo[key] = 1
		return true
	}
	var counts [26]int64
	for k := int64(0); k < length; k++ {
		counts[s1[i1+k]-97]++
		counts[s2[i2+k]-97]--
	}
	for c := 0; c < 26; c++ {
		if counts[c] != 0 {
			memo[key] = 0
			return false
		}
	}
	for split := int64(1); split < length; split++ {
		if scramble(s1, i1, s2, i2, split, memo, n) &&
			scramble(s1, i1+split, s2, i2+split, length-split, memo, n) {
			memo[key] = 1
			return true
		}
		if scramble(s1, i1, s2, i2+length-split, split, memo, n) &&
			scramble(s1, i1+split, s2, i2, length-split, memo, n) {
			memo[key] = 1
			return true
		}
	}
	memo[key] = 0
	return false
}

func one(length, seed int64) int64 {
	s1 := make([]byte, length)
	for j := int64(0); j < length; j++ {
		s1[j] = byte(97 + (j % 8))
	}
	s2 := make([]byte, length)
	for j := int64(0); j < length; j++ {
		s2[j] = s1[(j*5+seed)%length]
	}
	cells := length * length * (length + 1)
	memo := make([]int64, cells)
	for i := int64(0); i < cells; i++ {
		memo[i] = -1
	}
	var r int64 = 0
	if scramble(s1, 0, s2, 0, length, memo, length) {
		r = 1
	}
	h := r
	for i := int64(0); i < cells; i++ {
		h = (h*131 + (memo[i] + 2)) % 1000000007
	}
	return h
}

func main() {
	const length = 12
	const total = 60000
	var sum int64 = 0
	for k := int64(0); k < total; k++ {
		sum += one(length, k)
	}
	fmt.Println(sum)
}
