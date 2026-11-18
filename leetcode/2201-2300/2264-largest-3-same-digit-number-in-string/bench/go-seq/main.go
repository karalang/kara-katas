// LeetCode #2264: Largest 3-Same-Digit Number in String -- Go mirror of
// the ★ arm (good.kara): one pass over the bytes, the largest digit seen
// three times running, three times over or "". Output is byte-identical
// to good.kara.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

func largestGoodInteger(num string) string {
	best := -1
	for i := 2; i < len(num); i++ {
		if num[i-2] == num[i] && num[i-1] == num[i] {
			if best < 0 || int(num[i]) > best {
				best = int(num[i])
			}
		}
	}
	if best < 0 {
		return ""
	}
	return strings.Repeat(string(rune(best)), 3)
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2264

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var check int64
	for t := 0; t < 2000; t++ {
		digits := int64(10)
		if t%2 == 0 {
			digits = 4
		}
		var b strings.Builder
		for i := 0; i < 1000; i++ {
			b.WriteByte(byte('0' + nextRandom()%digits))
		}
		good := largestGoodInteger(b.String())
		score := int64(1000)
		if good != "" {
			score, _ = strconv.ParseInt(good, 10, 64)
		}
		check = (check*31 + score) % 1000000007
	}
	fmt.Printf("2000 numbers of 1000: checksum %d\n", check)
}
