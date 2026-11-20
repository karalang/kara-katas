// LeetCode #1208 bench, in Go: the ★ arm (a window over the letters,
// widened one letter a step and shrunk from the left while it costs more
// than the budget) on 16 pairs of strings of 100000 letters drawn once,
// then 10 rounds over the pairs with the budgets 0, 1000, 100000 and
// 1000000, every answer folded into a checksum.
package main

import (
	"fmt"
	"strings"
)

var seed int64 = 1208

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func equalSubstring(s, t string, maxCost int64) int64 {
	var best, cost int64
	left := 0
	for right := 0; right < len(s); right++ {
		cost += abs(int64(s[right]) - int64(t[right]))
		for cost > maxCost {
			cost -= abs(int64(s[left]) - int64(t[left]))
			left++
		}
		if w := int64(right - left + 1); w > best {
			best = w
		}
	}
	return best
}

func main() {
	type pair struct{ s, t string }
	pairs := make([]pair, 0, 16)
	for p := 0; p < 16; p++ {
		var s, t strings.Builder
		s.Grow(100000)
		t.Grow(100000)
		var spread int64 = 2
		for i := 0; i < 100000; i++ {
			if i%1000 == 0 {
				if nextRandom()%2 == 0 {
					spread = 2
				} else {
					spread = 25
				}
			}
			x := nextRandom() % 26
			y := (x + nextRandom()%(spread+1)) % 26
			s.WriteByte(byte('a' + x))
			t.WriteByte(byte('a' + y))
		}
		pairs = append(pairs, pair{s.String(), t.String()})
	}
	budgets := []int64{0, 1000, 100000, 1000000}
	var check int64
	for round := int64(0); round < 10; round++ {
		for _, p := range pairs {
			for _, c := range budgets {
				check = (check*131 + equalSubstring(p.s, p.t, c) + round) % 1000000007
			}
		}
	}
	fmt.Printf("10 rounds over 16 pairs of 100000 letters: checksum %d\n", check)
}
