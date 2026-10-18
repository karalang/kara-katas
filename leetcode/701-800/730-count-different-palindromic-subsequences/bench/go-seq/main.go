// LeetCode #730: Count Different Palindromic Subsequences -- by
// interval, with the next and previous copy of the end letter.
// Benchmark mirror of the Kara star arm: the count for each interval
// from the ones inside it.
package main

import "fmt"

const M = 1000000007

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func countPalindromicSubsequences(b []byte) int64 {
	n := int64(len(b))
	nextSame := make([]int64, n)
	prevSame := make([]int64, n)
	last := [4]int64{-1, -1, -1, -1}
	for i := range nextSame {
		nextSame[i] = n
	}
	for i := int64(0); i < n; i++ {
		c := b[i] - 'a'
		prevSame[i] = last[c]
		if last[c] >= 0 {
			nextSame[last[c]] = i
		}
		last[c] = i
	}
	count := make([][]int64, n)
	for i := range count {
		count[i] = make([]int64, n)
	}
	for i := n - 1; i >= 0; i-- {
		count[i][i] = 1
		for j := i + 1; j < n; j++ {
			var inner int64
			if i+1 <= j-1 {
				inner = count[i+1][j-1]
			}
			var v int64
			if b[i] != b[j] {
				v = count[i+1][j] + count[i][j-1] - inner
			} else {
				lo, hi := nextSame[i], prevSame[j]
				if lo > hi {
					v = 2*inner + 2
				} else if lo == hi {
					v = 2*inner + 1
				} else {
					var twice int64
					if lo+1 <= hi-1 {
						twice = count[lo+1][hi-1]
					}
					v = 2*inner - twice
				}
			}
			count[i][j] = ((v % M) + M) % M
		}
	}
	return count[0][n-1]
}

func main() {
	seed := int64(730)
	var sum int64
	s := make([]byte, 1000)
	for r := 0; r < 200; r++ {
		for i := range s {
			s[i] = byte('a' + nextRandom(&seed)%4)
		}
		sum = (sum + countPalindromicSubsequences(s)) % M
	}
	fmt.Printf("200 strings of 1000 letters: sum %d\n", sum)
}
