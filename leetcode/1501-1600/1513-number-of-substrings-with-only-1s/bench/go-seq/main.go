// LeetCode #1513: Number of Substrings With Only 1s -- the bench: 20
// strings of 500000 bits built once, then each counted five times by the
// ★ arm.
package main

import (
	"fmt"
	"strings"
)

const mod = 1000000007

func numSub(s string) int64 {
	var run, total int64
	for _, c := range s {
		if c == '1' {
			run++
			total += run
		} else {
			run = 0
		}
	}
	return total % mod
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1513)
	strs := make([]string, 20)
	for k := int64(0); k < 20; k++ {
		var b strings.Builder
		for i := 0; i < 500000; i++ {
			if nextRandom(&seed)%20 < k {
				b.WriteByte('1')
			} else {
				b.WriteByte('0')
			}
		}
		strs[k] = b.String()
	}
	var check int64
	for r := 0; r < 5; r++ {
		for _, s := range strs {
			check = (check*31 + numSub(s) + 1) % 1000000007
		}
	}
	fmt.Printf("100 counts over 20 strings of 500000 bits: checksum %d\n", check)
}
