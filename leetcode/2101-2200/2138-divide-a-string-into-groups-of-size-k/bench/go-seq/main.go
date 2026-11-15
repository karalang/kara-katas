// LeetCode #2138: Divide a String Into Groups of Size k -- the benchmark,
// the same algorithm as divide.kara.
package main

import (
	"fmt"
	"strings"
)

func divideString(s string, k int, fill byte) []string {
	n := len(s)
	groups := []string{}
	for start := 0; start < n; start += k {
		end := start + k
		if end > n {
			end = n
		}
		var b strings.Builder
		b.Grow(k)
		b.WriteString(s[start:end])
		for b.Len() < k {
			b.WriteByte(fill)
		}
		groups = append(groups, b.String())
	}
	return groups
}

var seed int64 = 2138

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const alphabet = "abcdefghijklmnopqrstuvwxyz"
	strs := make([][]byte, 1000)
	for i := range strs {
		strs[i] = make([]byte, 100)
		for j := range strs[i] {
			strs[i][j] = alphabet[nextRandom()%26]
		}
	}
	total, check := int64(0), int64(0)
	for r := 0; r < 100; r++ {
		for i := 0; i < 1000; i++ {
			at := nextRandom() % 100
			strs[i][at] = alphabet[nextRandom()%26]
			k := int(nextRandom()%100 + 1)
			fill := alphabet[nextRandom()%26]
			groups := divideString(string(strs[i]), k, fill)
			total += int64(len(groups))
			last := groups[len(groups)-1]
			for j := 0; j < len(last); j++ {
				check = (check*131 + int64(last[j])) % 1000000007
			}
		}
	}
	fmt.Printf("100000 solves: %d groups, checksum %d\n", total, check)
}
