// LeetCode #10 — Go seq bench peer for regex.kara. Same recursive
// matcher, same workload (N=8 pairs, K=10M iters), same sink as the
// Kara / Rust / C mirrors.

package main

import "fmt"

func isMatchAt(s []byte, i int, p []byte, j int) bool {
	n := len(s)
	m := len(p)

	if j == m {
		return i == n
	}

	firstMatch := i < n && (p[j] == s[i] || p[j] == '.')

	if j+1 < m && p[j+1] == '*' {
		return isMatchAt(s, i, p, j+2) ||
			(firstMatch && isMatchAt(s, i+1, p, j))
	}

	return firstMatch && isMatchAt(s, i+1, p, j+1)
}

func isMatch(s string, p string) bool {
	return isMatchAt([]byte(s), 0, []byte(p), 0)
}

func main() {
	const n int64 = 8
	const kIters int64 = 10_000_000

	strs := []string{
		"aa",
		"ab",
		"aab",
		"mississippi",
		"aaaaaaaaaab",
		"aaa",
		"abc",
		"aaab",
	}
	pats := []string{
		"a*",
		".*",
		"c*a*b",
		"mis*is*p*.",
		"a*a*a*a*a*b",
		"ab*a",
		"...",
		"a*b",
	}

	var sum int64
	for k := int64(0); k < kIters; k++ {
		idx := k % n
		if isMatch(strs[idx], pats[idx]) {
			sum++
		}
	}
	fmt.Println(sum)
}
