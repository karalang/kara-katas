// Benchmark: LeetCode #1092 Shortest Common Supersequence -- Go mirror of the
// ★ arm: the longest common subsequence's table, a slice of rows, walked
// back from the end. Same workload and sink as
// ../shortest_common_supersequence.kara.
package main

import "fmt"

func shortestCommonSupersequence(a, b string) string {
	x, y := []rune(a), []rune(b)
	n, m := len(x), len(y)
	lcs := make([][]int64, n+1)
	for i := range lcs {
		lcs[i] = make([]int64, m+1)
	}
	for i := 1; i <= n; i++ {
		for j := 1; j <= m; j++ {
			if x[i-1] == y[j-1] {
				lcs[i][j] = lcs[i-1][j-1] + 1
			} else {
				lcs[i][j] = max(lcs[i-1][j], lcs[i][j-1])
			}
		}
	}
	out := []rune{}
	i, j := n, m
	for i > 0 && j > 0 {
		if x[i-1] == y[j-1] {
			out = append(out, x[i-1])
			i--
			j--
		} else if lcs[i-1][j] >= lcs[i][j-1] {
			out = append(out, x[i-1])
			i--
		} else {
			out = append(out, y[j-1])
			j--
		}
	}
	for ; i > 0; i-- {
		out = append(out, x[i-1])
	}
	for ; j > 0; j-- {
		out = append(out, y[j-1])
	}
	for lo, hi := 0, len(out)-1; lo < hi; lo, hi = lo+1, hi-1 {
		out[lo], out[hi] = out[hi], out[lo]
	}
	return string(out)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomWord(seed *int64, n int, letters int64) string {
	w := make([]rune, 0, n)
	for i := 0; i < n; i++ {
		w = append(w, rune(97+nextRandom(seed)%letters))
	}
	return string(w)
}

func main() {
	seed := int64(1092)
	type pair struct{ a, b string }
	pairs := []pair{}
	for k := int64(0); k < 50; k++ {
		letters := 2 + k%25
		a := randomWord(&seed, 1000, letters)
		b := randomWord(&seed, 1000, letters)
		pairs = append(pairs, pair{a, b})
	}
	var total, check int64
	for round := 0; round < 4; round++ {
		for _, p := range pairs {
			s := []rune(shortestCommonSupersequence(p.a, p.b))
			n := int64(len(s))
			total += n
			check = (check*31 + n) % 1000000007
			check = (check*31 + int64(s[n/3])) % 1000000007
			check = (check*31 + int64(s[2*n/3])) % 1000000007
		}
	}
	fmt.Printf("4 rounds over 50 pairs of 1000 letters: lengths sum to %d, checksum %d\n", total, check)
}
