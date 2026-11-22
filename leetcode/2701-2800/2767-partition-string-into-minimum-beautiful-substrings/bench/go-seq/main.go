// LeetCode #2767: Partition String Into Minimum Beautiful Substrings --
// the bench in Go: the ★ arm over 100000 strings of 15 binary digits, all
// drawn first, then each answered 5 times.
package main

import (
	"fmt"
	"strconv"
)

func isPowerOfFive(v int64) bool {
	for v > 1 && v%5 == 0 {
		v /= 5
	}
	return v == 1
}

func minimumBeautifulSubstrings(s string) int64 {
	n := len(s)
	best := make([]int64, n+1)
	for i := range best {
		best[i] = -1
	}
	best[0] = 0
	for i := 1; i <= n; i++ {
		for j := 0; j < i; j++ {
			if best[j] < 0 || s[j:j+1] != "1" {
				continue
			}
			value, _ := strconv.ParseInt(s[j:i], 2, 64)
			if isPowerOfFive(value) && (best[i] < 0 || best[j]+1 < best[i]) {
				best[i] = best[j] + 1
			}
		}
	}
	return best[n]
}

var seed int64 = 2767

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count := 100000
	rounds := 5
	powers := []string{"1", "101", "11001", "1111101", "1001110001", "110000110101", "11110100001001"}
	strings := make([]string, 0, count)
	for c := 0; c < count; c++ {
		s := ""
		for {
			p := powers[nextRandom()%7]
			if len(s)+len(p) > 15 {
				break
			}
			s += p
		}
		for len(s) < 15 {
			if nextRandom()%2 == 1 {
				s += "1"
			} else {
				s += "0"
			}
		}
		if nextRandom()%2 == 1 {
			k := nextRandom() % 15
			flipped := "1"
			if s[k:k+1] == "1" {
				flipped = "0"
			}
			s = s[:k] + flipped + s[k+1:]
		}
		strings = append(strings, s)
	}
	var split, pieces, check int64
	for r := 0; r < rounds; r++ {
		for _, s := range strings {
			a := minimumBeautifulSubstrings(s)
			if a > 0 {
				split++
				pieces += a
			}
			check = (check*31 + a + 1 + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d strings of 15, %d rounds: %d split, pieces sum to %d, checksum %d\n", count, rounds, split, pieces, check)
}
