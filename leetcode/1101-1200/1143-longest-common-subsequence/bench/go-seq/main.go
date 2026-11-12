// LeetCode #1143: Longest Common Subsequence -- the bench in Go, the ★
// arm's algorithm.
package main

import "fmt"

func longestCommonSubsequence(text1, text2 string) int64 {
	a, b := []rune(text1), []rune(text2)
	m, n := len(a), len(b)
	best := make([][]int64, m+1)
	for i := range best {
		best[i] = make([]int64, n+1)
	}
	for i := 1; i <= m; i++ {
		for j := 1; j <= n; j++ {
			if a[i-1] == b[j-1] {
				best[i][j] = best[i-1][j-1] + 1
			} else {
				best[i][j] = max(best[i-1][j], best[i][j-1])
			}
		}
	}
	return best[m][n]
}

var seed int64 = 1143

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	letters := []rune("abcd")
	texts := make([][]rune, 20)
	for t := range texts {
		texts[t] = make([]rune, 1000)
		for i := range texts[t] {
			texts[t][i] = letters[nextRandom()%4]
		}
	}
	var total, check int64
	for round := 0; round < 10; round++ {
		for p := 0; p < 10; p++ {
			for t := 2 * p; t <= 2*p+1; t++ {
				at := nextRandom() % 1000
				texts[t][at] = letters[nextRandom()%4]
			}
			answer := longestCommonSubsequence(string(texts[2*p]), string(texts[2*p+1]))
			total += answer
			check = (check*131 + answer + 1) % 1000000007
		}
	}
	fmt.Printf("10 rounds over 10 pairs of 1000 letters: answers total %d, checksum %d\n", total, check)
}
