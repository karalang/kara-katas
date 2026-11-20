// LeetCode #1682: Longest Palindromic Subsequence II -- the bench's Go
// mirror: the ★ arm on 200 random strings of 250 letters from the first 4
// of the alphabet, all drawn first, each answered 2 times.

package main

import "fmt"

func longestPalindromeSubseq(s string) int32 {
	n := len(s)
	if n == 0 {
		return 0
	}
	best := make([][][26]int32, n)
	for i := range best {
		best[i] = make([][26]int32, n)
	}
	for i := n - 1; i >= 0; i-- {
		for j := i + 1; j < n; j++ {
			for c := 0; c < 26; c++ {
				if int(s[i]-'a') == c && int(s[j]-'a') == c {
					var inside int32
					if i+1 < j-1 {
						for d := 0; d < 26; d++ {
							if d != c {
								inside = max(inside, best[i+1][j-1][d])
							}
						}
					}
					best[i][j][c] = inside + 2
				} else {
					best[i][j][c] = max(best[i+1][j][c], best[i][j-1][c])
				}
			}
		}
	}
	var answer int32
	for _, v := range best[0][n-1] {
		answer = max(answer, v)
	}
	return answer
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1682

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count = 200
	const n = 250
	const rounds = 2
	alphabet := "abcd"
	strings := make([]string, 0, count)
	for c := 0; c < count; c++ {
		b := make([]byte, n)
		for i := range b {
			b[i] = alphabet[nextRandom()%4]
		}
		strings = append(strings, string(b))
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, s := range strings {
			answer := int64(longestPalindromeSubseq(s))
			total += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d strings of %d letters, %d rounds: answers sum to %d, checksum %d\n", count, n, rounds, total, check)
}
