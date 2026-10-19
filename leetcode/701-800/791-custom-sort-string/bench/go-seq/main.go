// LeetCode 791 — Custom Sort String: the bench, in Go.
// Mirrors custom_sort_string.kara: count the letters, write out order's
// letters, then the rest in place, into a new string each round.
package main

import (
	"fmt"
	"strings"
)

func customSortString(order, s string) string {
	var count [26]int64
	for i := 0; i < len(s); i++ {
		count[s[i]-'a']++
	}
	var named [26]bool
	var out strings.Builder
	for i := 0; i < len(order); i++ {
		at := order[i] - 'a'
		named[at] = true
		for k := int64(0); k < count[at]; k++ {
			out.WriteByte(order[i])
		}
	}
	for i := 0; i < len(s); i++ {
		if !named[s[i]-'a'] {
			out.WriteByte(s[i])
		}
	}
	return out.String()
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	letters := "abcdefghijklmnopqrstuvwxyz"
	seed := int64(791)
	orders := make([]string, 0, 64)
	strs := make([]string, 0, 64)
	for k := 0; k < 64; k++ {
		pool := []byte(letters)
		for i := int64(25); i > 0; i-- {
			j := nextRandom(&seed) % (i + 1)
			pool[i], pool[j] = pool[j], pool[i]
		}
		size := 1 + nextRandom(&seed)%26
		orders = append(orders, string(pool[:size]))
		b := make([]byte, 200)
		for i := range b {
			b[i] = letters[nextRandom(&seed)%26]
		}
		strs = append(strs, string(b))
	}
	rounds := int64(1000000)
	total, check := int64(0), int64(0)
	for r := int64(0); r < rounds; r++ {
		answer := customSortString(orders[r%64], strs[(r/64)%64])
		total += int64(len(answer))
		if r%1000 == 0 {
			for i := 0; i < len(answer); i++ {
				check = (check*131 + int64(answer[i])) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds of 200-letter strings: %d letters, checksum %d\n", rounds, total, check)
}
