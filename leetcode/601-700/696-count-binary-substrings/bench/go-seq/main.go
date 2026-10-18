// LeetCode #696: Count Binary Substrings -- bench program, Go mirror of the ★ arm.
package main

import (
	"fmt"
	"strings"
)

var seed int64 = 696

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func countBinarySubstrings(s string) int64 {
	var before, current, count int64 = 0, 1, 0
	for i := 1; i < len(s); i++ {
		if s[i] == s[i-1] {
			current++
		} else {
			count += min(before, current)
			before = current
			current = 1
		}
	}
	return count + min(before, current)
}

func main() {
	strs := []string{}
	for k := int64(0); k < 20; k++ {
		longest := 1 + 2*k
		var b strings.Builder
		bit := 0
		for b.Len() < 100000 {
			run := 1 + nextRandom()%longest
			for r := int64(0); r < run; r++ {
				if b.Len() < 100000 {
					if bit == 0 {
						b.WriteByte('0')
					} else {
						b.WriteByte('1')
					}
				}
			}
			bit = 1 - bit
		}
		strs = append(strs, b.String())
	}
	rounds := 150
	var total, checksum int64
	for r := 0; r < rounds; r++ {
		for _, s := range strs {
			c := countBinarySubstrings(s)
			total += c
			checksum = (checksum*31 + c) % 1000000007
		}
	}
	fmt.Printf("%d rounds of 20 strings of 100000: %d substrings counted, checksum %d\n", rounds, total, checksum)
}
