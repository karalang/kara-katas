// LeetCode #2522: Partition String Into Substrings With Values at Most K --
// Go mirror of the benchmark (greedy.kara): the same strings, passes, order
// and checksum.
package main

import (
	"fmt"
	"strings"
)

func minimumPartition(s string, k int64) int64 {
	parts, value := int64(1), int64(0)
	for i := 0; i < len(s); i++ {
		d := int64(s[i] - '0')
		if d > k {
			return -1
		}
		value = value*10 + d
		if value > k {
			parts++
			value = d
		}
	}
	return parts
}

var seed int64 = 2522

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	all := make([]string, 20)
	for t := range all {
		var b strings.Builder
		for i := 0; i < 100000; i++ {
			b.WriteByte(byte('0' + nextRandom()%9 + 1))
		}
		all[t] = b.String()
	}
	const passes = 50
	var check int64
	for p := int64(0); p < passes; p++ {
		for _, s := range all {
			check = (check*31 + minimumPartition(s, check%999999992+9) + p) % 1000000007
		}
	}
	fmt.Printf("%d passes over 20 strings of 10^5 digits: checksum %d\n", passes, check)
}
