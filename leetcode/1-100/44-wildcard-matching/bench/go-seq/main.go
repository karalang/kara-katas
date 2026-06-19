// LeetCode #44 bench mirror — Go, the greedy two-pointer matcher (★).
//
// Mirrors bench/wildcard_matching.kara: one cursor in each of s and p, with star/matched
// scalars for O(1) backtracking. Build s and a multi-star pattern p once, punch one s slot
// per iteration, fold the boolean into a rolling checksum. Same workload + sink as every
// other mirror.
package main

import "fmt"

func isMatch(s []byte, p []byte) bool {
	n := int64(len(s))
	m := int64(len(p))
	var i, j int64 = 0, 0
	var star int64 = -1
	var matched int64 = 0
	for i < n {
		if j < m && (p[j] == '?' || p[j] == s[i]) {
			i++
			j++
		} else if j < m && p[j] == '*' {
			star = j
			matched = i
			j++
		} else if star != -1 {
			matched++
			i = matched
			j = star + 1
		} else {
			return false
		}
	}
	for j < m && p[j] == '*' {
		j++
	}
	return j == m
}

func main() {
	var total int64 = 300000
	var modulus int64 = 1000000007
	var n int64 = 240

	s := make([]byte, n)
	for a := int64(0); a < n; a++ {
		s[a] = byte('a' + (a % 3))
	}
	p := make([]byte, 0, 33)
	for g := 0; g < 8; g++ {
		p = append(p, '*', 'a', 'b', 'c')
	}
	p = append(p, '*')

	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		s[k%n] = byte('a' + (k % 4))
		var bit int64 = 0
		if isMatch(s, p) {
			bit = 1
		}
		acc = (acc*131 + bit) % modulus
	}

	fmt.Println(acc)
}
