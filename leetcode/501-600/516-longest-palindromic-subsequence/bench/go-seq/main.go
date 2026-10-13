// Benchmark for #516: Go mirror of the ★ arm (a table over substrings);
// see ../longest_palindrome_subseq.kara.
package main

import "fmt"

func longestPalindromeSubseq(b []byte) int64 {
	n := len(b)
	best := make([][]int64, n)
	for i := range best {
		best[i] = make([]int64, n)
	}
	for i := n - 1; i >= 0; i-- {
		best[i][i] = 1
		for j := i + 1; j < n; j++ {
			if b[i] == b[j] {
				best[i][j] = best[i+1][j-1] + 2
			} else {
				best[i][j] = max(best[i+1][j], best[i][j-1])
			}
		}
	}
	return best[0][n-1]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 120 random strings of 1,000 letters (the problem's most), from the
	// first 4 or all 26 in turn, solved once each.
	seed := int64(516)
	strings := 120
	var total, checksum int64
	for t := 0; t < strings; t++ {
		letters := int64(26)
		if t%2 == 0 {
			letters = 4
		}
		s := make([]byte, 0, 1000)
		for i := 0; i < 1000; i++ {
			s = append(s, byte('a'+nextRandom(&seed)%letters))
		}
		v := longestPalindromeSubseq(s)
		total += v
		checksum = (checksum*31 + v) % 1000000007
	}
	fmt.Printf("%d strings of 1000 letters: %d in all, checksum %d\n", strings, total, checksum)
}
