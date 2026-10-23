// LeetCode #926: Flip String to Monotone Increasing -- bench: one pass.
// Mirrors min_flips_mono_incr.kara.
package main

import "fmt"

func minFlipsMonoIncr(s string) int64 {
	var flips, ones int64
	for i := 0; i < len(s); i++ {
		if s[i] == '1' {
			ones++
		} else {
			flips = min(flips+1, ones)
		}
	}
	return flips
}

var seed int64 = 926

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const rounds, count, n = 20, 100, 100000
	// count strings of n characters, built once, leaning from 0 to 1
	strings := make([]string, count)
	for i := range strings {
		lean := int64(i % 101)
		b := make([]byte, n)
		for j := range b {
			if nextRandom()%100 < lean {
				b[j] = '1'
			} else {
				b[j] = '0'
			}
		}
		strings[i] = string(b)
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		// each round visits every string, starting from a different one
		for i := 0; i < count; i++ {
			a := minFlipsMonoIncr(strings[(r+i)%count])
			total += a
			check = (check*1000003 + a) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d strings of %d: answers summing to %d, checksum %d\n", rounds, count, n, total, check)
}
