// LeetCode #2414: Length of the Longest Alphabetical Continuous Substring
// -- the bench, the ★ arm in Go: one scan, the run growing while each
// letter follows the one before, the longest run kept.

package main

import "fmt"

func longestContinuousSubstring(s string) int64 {
	var run, best int64 = 1, 1
	for i := 1; i < len(s); i++ {
		if s[i] == s[i-1]+1 {
			run++
			if run > best {
				best = run
			}
		} else {
			run = 1
		}
	}
	return best
}

var seed int64 = 2414

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	strings := make([]string, 0, 10)
	for i := int64(0); i < 10; i++ {
		b := make([]byte, 0, 100000)
		for j := 0; j < 100000; j++ {
			if j > 0 && b[j-1] < 'z' && nextRandom()%(i+2) != 0 {
				b = append(b, b[j-1]+1)
			} else {
				b = append(b, byte('a'+nextRandom()%26))
			}
		}
		strings = append(strings, string(b))
	}
	var check int64
	for p := int64(0); p < 200; p++ {
		for _, s := range strings {
			check = (check*31 + longestContinuousSubstring(s) + p) % 1000000007
		}
	}
	fmt.Printf("200 passes over 10 strings of 10^5 letters: checksum %d\n", check)
}
