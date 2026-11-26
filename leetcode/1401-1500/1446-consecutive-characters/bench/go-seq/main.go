// LeetCode #1446 Consecutive Characters: the bench, a mirror of
// max_power.kara.
package main

import (
	"fmt"
	"strings"
)

func maxPower(s string) int {
	// the length of the run the letter so far ends, and the longest run
	best := 0
	run := 0
	last := ' '
	for _, ch := range s {
		if ch == last {
			run += 1
		} else {
			run = 1
			last = ch
		}
		best = max(best, run)
	}
	return best
}

func main() {
	// 200 strings of 10^5 letters, each drawn from the first 2 to 4 of the
	// alphabet, each string's power asked 10 times, the powers folded to a
	// checksum
	var seed int64 = 1446
	strs := make([]string, 0, 200)
	for j := 0; j < 200; j++ {
		k := int64(2 + j%3)
		var b strings.Builder
		for i := 0; i < 100000; i++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			b.WriteByte(byte('a' + seed/65536%k))
		}
		strs = append(strs, b.String())
	}
	var check int64 = 0
	for r := 0; r < 10; r++ {
		for _, s := range strs {
			check = (check*131 + int64(maxPower(s))) % 1000000007
		}
	}
	fmt.Printf("2000 strings of 10^5 letters: checksum %d\n", check)
}
