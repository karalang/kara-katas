// LeetCode #2002: Maximum Product of the Length of Two Palindromic
// Subsequences -- the benchmark, the same algorithm as palindromes.kara.
package main

import (
	"bytes"
	"fmt"
	"strings"
)

func longestPalindrome(chars []byte) int64 {
	n := len(chars)
	if n == 0 {
		return 0
	}
	dp := make([][]int64, n)
	for i := range dp {
		dp[i] = make([]int64, n)
	}
	for i := n - 1; i >= 0; i-- {
		dp[i][i] = 1
		for j := i + 1; j < n; j++ {
			if chars[i] == chars[j] {
				dp[i][j] = dp[i+1][j-1] + 2
			} else {
				dp[i][j] = max(dp[i+1][j], dp[i][j-1])
			}
		}
	}
	return dp[0][n-1]
}

func maxProduct(s string) int64 {
	b := []byte(s)
	n := len(b)
	var best int64
	for mask := 1; mask < 1<<n; mask++ {
		picked := []byte{}
		rest := []byte{}
		for i := 0; i < n; i++ {
			if (mask>>i)&1 == 1 {
				picked = append(picked, b[i])
			} else {
				rest = append(rest, b[i])
			}
		}
		reversed := append([]byte{}, picked...)
		for i, j := 0, len(reversed)-1; i < j; i, j = i+1, j-1 {
			reversed[i], reversed[j] = reversed[j], reversed[i]
		}
		if bytes.Equal(picked, reversed) {
			best = max(best, int64(len(picked))*longestPalindrome(rest))
		}
	}
	return best
}

var seed int64 = 2002

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	strs := []string{}
	for a := int64(0); a < 3000; a++ {
		var sb strings.Builder
		for i := 0; i < 12; i++ {
			sb.WriteByte(byte(97 + nextRandom()%(2+a%4)))
		}
		strs = append(strs, sb.String())
	}
	var sum, check int64
	for _, s := range strs {
		answer := maxProduct(s)
		sum += answer
		check = (check*31 + answer) % 1000000007
	}
	fmt.Printf("%d strings: sum %d, checksum %d\n", len(strs), sum, check)
}
