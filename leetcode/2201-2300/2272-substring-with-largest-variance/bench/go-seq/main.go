// LeetCode #2272: Substring With Largest Variance -- the bench, the ★ arm.
package main

import (
	"fmt"
	"math"
	"strings"
)

func largestVariance(s string) int64 {
	var seen [26]bool
	for i := 0; i < len(s); i++ {
		seen[s[i]-'a'] = true
	}
	var best int64
	for a := byte('a'); a <= 'z'; a++ {
		for b := byte('a'); b <= 'z'; b++ {
			if a == b || !seen[a-'a'] || !seen[b-'a'] {
				continue
			}
			var diff int64
			withB := int64(math.MinInt64 / 2)
			for i := 0; i < len(s); i++ {
				c := s[i]
				if c == a {
					diff++
					withB++
				} else if c == b {
					withB = diff - 1
					diff--
					if diff < 0 {
						diff = 0
					}
				}
				if withB > best {
					best = withB
				}
			}
		}
	}
	return best
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2272

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	ks := []int64{3, 5, 10, 26}
	var check int64
	for t := 0; t < 40; t++ {
		k := ks[t%4]
		var b strings.Builder
		for i := 0; i < 10000; i++ {
			b.WriteByte(byte('a' + nextRandom()%k))
		}
		check = (check*31 + largestVariance(b.String())) % 1000000007
	}
	fmt.Printf("40 strings of 10^4: checksum %d\n", check)
}
