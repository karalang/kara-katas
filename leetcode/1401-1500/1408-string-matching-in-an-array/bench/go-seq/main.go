// LeetCode #1408 bench, Go: the same check of every word against every
// other, workload and checksum as string_matching.kara.
package main

import (
	"fmt"
	"strings"
)

func stringMatching(words []string) []string {
	found := []string{}
	for _, w := range words {
		for _, other := range words {
			if other != w && strings.Contains(other, w) {
				found = append(found, w)
				break
			}
		}
	}
	return found
}

func main() {
	var seed int64 = 1408
	pool := make([]string, 0, 10000)
	for i := 0; i < 10000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		size := 1 + seed/65536%12
		var b strings.Builder
		for k := int64(0); k < size; k++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			b.WriteByte(byte('a' + seed/65536%3))
		}
		pool = append(pool, b.String())
	}
	var check int64
	for r := int64(0); r < 2000; r++ {
		at := (check + r*7919) % 9901
		words := []string{}
		for _, w := range pool[at : at+100] {
			seen := false
			for _, x := range words {
				if x == w {
					seen = true
					break
				}
			}
			if !seen {
				words = append(words, w)
			}
		}
		found := stringMatching(words)
		var letters int64
		for _, w := range found {
			letters += int64(len(w))
		}
		check = (check*131 + int64(len(found))*1000 + letters) % 1000000007
	}
	fmt.Printf("2000 windows of 100 words: checksum %d\n", check)
}
