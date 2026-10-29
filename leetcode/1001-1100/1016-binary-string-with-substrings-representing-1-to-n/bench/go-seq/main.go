// LeetCode #1016: Binary String With Substrings Representing 1 To N --
// bench
// Mirrors ../query.kara; see ../../README.md § Benchmarks.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

func queryString(s string, n int64) bool {
	if n-n/2 > 2*int64(len(s)) {
		return false
	}
	for x := n; x > n/2; x-- {
		if !strings.Contains(s, strconv.FormatInt(x, 2)) {
			return false
		}
	}
	return true
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	stringsCount := 200
	length := 1000
	most := int64(400)
	seed := int64(1016)
	holds := 0
	var check int64
	for t := 0; t < stringsCount; t++ {
		var b strings.Builder
		for i := 0; i < length; i++ {
			if nextRandom(&seed)%2 == 1 {
				b.WriteByte('1')
			} else {
				b.WriteByte('0')
			}
		}
		s := b.String()
		for n := int64(1); n < most+1; n++ {
			answer := queryString(s, n)
			var bit int64
			if answer {
				holds++
				bit = 1
			}
			check = (check*2 + bit) % 1000000007
		}
	}
	fmt.Printf("%d strings of %d bits, n = 1..%d: %d hold, checksum %d\n", stringsCount, length, most, holds, check)
}
