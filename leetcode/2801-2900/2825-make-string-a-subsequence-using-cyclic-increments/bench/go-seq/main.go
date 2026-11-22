// LeetCode #2825: Make String a Subsequence Using Cyclic Increments --
// the bench's Go mirror of the ★ arm: two pointers over the bytes.
package main

import "fmt"

func canMakeSubsequence(a, b string) bool {
	j := 0
	for i := 0; i < len(a); i++ {
		if j == len(b) {
			break
		}
		c := a[i]
		next := c + 1
		if c == 'z' {
			next = 'a'
		}
		if c == b[j] || next == b[j] {
			j++
		}
	}
	return j == len(b)
}

var seed int64 = 2825

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func letters(n, from, width int64) string {
	s := make([]byte, n)
	for i := range s {
		s[i] = byte((from+nextRandom()%width)%26 + 97)
	}
	return string(s)
}

func main() {
	count, rounds := 100, 50
	s1 := make([]string, count)
	s2 := make([]string, count)
	for c := 0; c < count; c++ {
		s1[c] = letters(100000, 23, 6)
		m := (nextRandom()*32768+nextRandom())%50000 + 1
		s2[c] = letters(m, 23, 6)
	}
	var yes, check int64
	for r := 0; r < rounds; r++ {
		for c := 0; c < count; c++ {
			a := canMakeSubsequence(s1[c], s2[c])
			bit := int64(0)
			if a {
				yes++
				bit = 1
			}
			check = (check*31 + bit + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d pairs of 100000, %d rounds: %d true, checksum %d\n", count, rounds, yes, check)
}
