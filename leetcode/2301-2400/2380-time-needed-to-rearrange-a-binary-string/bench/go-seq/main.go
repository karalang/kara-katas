// LeetCode #2380: Time Needed to Rearrange a Binary String -- the bench,
// the ★ arm in Go: one pass, each 1 after some 0 taking the larger of one
// more second than the 1 before it and the 0s before it.
package main

import "fmt"

func secondsToRemoveOccurrences(s string) int64 {
	zeros, seconds := int64(0), int64(0)
	for i := 0; i < len(s); i++ {
		if s[i] == '0' {
			zeros++
		} else if zeros > 0 {
			seconds = max(seconds+1, zeros)
		}
	}
	return seconds
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 100 strings of 1000 digits, string s 1 with a chance of 1 + s % 10
	// in 12; pass p asks for string (s + 7 p) % 100 in turn
	seed := int64(2380)
	strings := make([]string, 0, 100)
	for s := int64(0); s < 100; s++ {
		digits := make([]byte, 1000)
		for i := range digits {
			if nextRandom(&seed)%12 < 1+s%10 {
				digits[i] = '1'
			} else {
				digits[i] = '0'
			}
		}
		strings = append(strings, string(digits))
	}
	check := int64(0)
	for p := int64(0); p < 500; p++ {
		for s := int64(0); s < 100; s++ {
			check = (check*31 + secondsToRemoveOccurrences(strings[(s+7*p)%100]) + p) % 1000000007
		}
	}
	fmt.Printf("500 passes over 100 strings of 1000 digits: checksum %d\n", check)
}
