// LeetCode #2311: Longest Binary Subsequence Less Than or Equal to K --
// the bench, the ★ arm in Go. Greedy from the right: every 0 taken, and
// a 1 taken when its place still leaves the value at most k.
package main

import "fmt"

func longestSubsequence(s string, k int64) int64 {
	var value, taken int64
	for i := len(s) - 1; i >= 0; i-- {
		if s[i] == '0' {
			taken++
		} else if taken < 31 && value+(int64(1)<<taken) <= k {
			value += int64(1) << taken
			taken++
		}
	}
	return taken
}

var seed int64 = 2311

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	strings := make([]string, 1000)
	for a := range strings {
		odds := nextRandom()%8 + 1
		s := make([]byte, 1000)
		for i := range s {
			if nextRandom()%odds == 0 {
				s[i] = '1'
			} else {
				s[i] = '0'
			}
		}
		strings[a] = string(s)
	}
	var check int64
	for p := int64(0); p < 100; p++ {
		for a := int64(0); a < 1000; a++ {
			check = (check*31 + longestSubsequence(strings[a], 10000000*(p+1)+a)) % 1000000007
		}
	}
	fmt.Printf("100 passes over 1000 strings of 1000 bits: checksum %d\n", check)
}
