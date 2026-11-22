// LeetCode #2864: Maximum Odd Binary Number -- the bench, as odd.kara:
// 10000 strings of 100 bits, each answered 50 times, every answer folded
// into the checksum byte by byte.
package main

import (
	"fmt"
	"strings"
)

func maximumOddBinaryNumber(s string) string {
	ones := strings.Count(s, "1")
	zeros := len(s) - ones
	return strings.Repeat("1", ones-1) + strings.Repeat("0", zeros) + "1"
}

var seed int64 = 2864

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds, n = 10000, 50, 100
	strs := make([]string, 0, count)
	for c := 0; c < count; c++ {
		bits := make([]byte, n)
		for i := range bits {
			if nextRandom()%3 == 0 {
				bits[i] = '1'
			} else {
				bits[i] = '0'
			}
		}
		bits[nextRandom()%n] = '1'
		strs = append(strs, string(bits))
	}
	var onesTotal, check int64
	for r := int64(0); r < rounds; r++ {
		for _, s := range strs {
			best := maximumOddBinaryNumber(s)
			onesTotal += int64(strings.Count(best, "1"))
			h := (check + r) % 1000000007
			for i := 0; i < len(best); i++ {
				h = (h*31 + int64(best[i])) % 1000000007
			}
			check = h
		}
	}
	fmt.Printf("%d strings of %d, %d rounds: %d ones, checksum %d\n", count, n, rounds, onesTotal, check)
}
