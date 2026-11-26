// LeetCode #1771: Maximize Palindrome Length From Subsequences -- the bench
// in Go, mirroring longest_palindrome.kara: the longest palindromic
// subsequence of every stretch of the two words joined.
package main

import (
	"fmt"
	"strings"
)

func longestPalindrome(word1, word2 string) int32 {
	s := word1 + word2
	n := len(s)
	split := len(word1)
	dp := make([][]int32, n)
	for i := range dp {
		dp[i] = make([]int32, n)
	}
	var best int32
	for i := n - 1; i >= 0; i-- {
		dp[i][i] = 1
		for j := i + 1; j < n; j++ {
			if s[i] == s[j] {
				dp[i][j] = dp[i+1][j-1] + 2
				if i < split && j >= split {
					best = max(best, dp[i][j])
				}
			} else {
				dp[i][j] = max(dp[i+1][j], dp[i][j-1])
			}
		}
	}
	return best
}

var seed int64 = 1771

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	words := make([]string, 100)
	for w := range words {
		letters := 2 + nextRandom()%25
		var b strings.Builder
		for i := 0; i < 1000; i++ {
			b.WriteByte(byte(97 + nextRandom()%letters))
		}
		words[w] = b.String()
	}
	var check int64
	for call := int64(0); call < 40; call++ {
		a := (check + call*7919) % 100
		b := (check/100 + call*31 + 1) % 100
		check = (check*31 + int64(longestPalindrome(words[a], words[b]))) % 1000000007
	}
	fmt.Printf("40 calls over 100 words: checksum %d\n", check)
}
