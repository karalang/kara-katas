// LeetCode #2243: Calculate Digit Sum of a String -- the benchmark's Go
// mirror of digits.kara: while the string is longer than k, it is
// rebuilt group by group, each group's digits summed and the sum written
// back.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

func digitSum(s string, k int) string {
	current := s
	for len(current) > k {
		var next strings.Builder
		for start := 0; start < len(current); {
			end := min(start+k, len(current))
			sum := int64(0)
			for _, ch := range current[start:end] {
				sum += int64(ch - '0')
			}
			next.WriteString(strconv.FormatInt(sum, 10))
			start = end
		}
		current = next.String()
	}
	return current
}

var seed int64 = 2243

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func digitsOf() string {
	b := make([]byte, 100)
	for i := range b {
		b[i] = byte('0' + nextRandom()%10)
	}
	return string(b)
}

func main() {
	strs := make([]string, 1000)
	for i := range strs {
		strs[i] = digitsOf()
	}
	check := int64(0)
	for pass := 0; pass < 200; pass++ {
		at := nextRandom() % 1000
		strs[at] = digitsOf()
		k := pass%4 + 2
		for _, s := range strs {
			for _, ch := range digitSum(s, k) {
				check = (check*31 + int64(ch)) % 1000000007
			}
		}
	}
	fmt.Printf("200 passes over 1000 strings: checksum %d\n", check)
}
