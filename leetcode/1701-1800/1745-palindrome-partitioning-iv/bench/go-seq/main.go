// LeetCode #1745: Palindrome Partitioning IV -- the bench (palin.kara in
// Go): a table of palindromes, then every pair of cuts.
package main

import (
	"fmt"
	"strings"
)

func checkPartitioning(s string) bool {
	b := []byte(s)
	n := len(b)
	is := make([][]bool, n)
	for i := range is {
		is[i] = make([]bool, n)
	}
	for i := n - 1; i >= 0; i-- {
		for j := i; j < n; j++ {
			is[i][j] = b[i] == b[j] && (j-i < 2 || is[i+1][j-1])
		}
	}
	for i := 1; i < n-1; i++ {
		if is[0][i-1] {
			for j := i; j < n-1; j++ {
				if is[i][j] && is[j+1][n-1] {
					return true
				}
			}
		}
	}
	return false
}

var seed int64 = 1745

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func letter() byte {
	if nextRandom()%2 == 0 {
		return 'a'
	}
	return 'b'
}

func palindrome(n int64) string {
	half := make([]byte, (n+1)/2)
	for i := range half {
		half[i] = letter()
	}
	var text strings.Builder
	text.Write(half)
	for i := n/2 - 1; i >= 0; i-- {
		text.WriteByte(half[i])
	}
	return text.String()
}

func main() {
	const count, rounds, n = 20, 5, 2000
	all := make([]string, 0, count)
	for k := 0; k < count; k++ {
		if k%2 == 0 {
			a := nextRandom()%(n-2) + 1
			b := nextRandom()%(n-a-1) + 1
			first := palindrome(a)
			second := palindrome(b)
			third := palindrome(n - a - b)
			all = append(all, first+second+third)
		} else {
			s := make([]byte, n)
			for i := range s {
				s[i] = letter()
			}
			all = append(all, string(s))
		}
	}
	var yes, check int64
	for r := int64(0); r < rounds; r++ {
		for k, s := range all {
			var bit int64
			if checkPartitioning(s) {
				bit = 1
			}
			yes += bit
			check = (check*3 + bit + int64(k) + r) % 1000000007
		}
	}
	fmt.Printf("%d strings of %d letters, %d rounds: %d split, checksum %d\n", count, n, rounds, yes, check)
}
