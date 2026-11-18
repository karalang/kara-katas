// LeetCode #1624: Largest Substring Between Two Equal Characters -- the
// bench in Go, mirroring gap.kara: one pass over the characters, the
// first index of each letter, and at every later sight the gap back to it.
package main

import (
	"fmt"
	"strings"
)

func maxLengthBetweenEqualCharacters(s string) int32 {
	var first [26]int64
	for k := range first {
		first[k] = -1
	}
	best := int64(-1)
	i := int64(0)
	for _, c := range s {
		letter := c - 'a'
		if first[letter] == -1 {
			first[letter] = i
		} else if i-first[letter]-1 > best {
			best = i - first[letter] - 1
		}
		i++
	}
	return int32(best)
}

var seed int64 = 1624

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	all := make([]string, 0, 100000)
	for k := 0; k < 100000; k++ {
		n := nextRandom()%300 + 1
		var b strings.Builder
		for i := int64(0); i < n; i++ {
			b.WriteByte(byte('a' + nextRandom()%26))
		}
		all = append(all, b.String())
	}
	var check, total int64
	for _, s := range all {
		got := int64(maxLengthBetweenEqualCharacters(s))
		total += got
		check = (check*31 + got + 1) % 1000000007
	}
	fmt.Printf("100000 random strings: answers sum to %d, checksum %d\n", total, check)
}
