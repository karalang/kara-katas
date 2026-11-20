// LeetCode #1229 bench: the ★ arm in Go, over the same 50 pairs of
// schedules and 10 durations as the Kāra bench.
package main

import (
	"fmt"
	"sort"
)

func minAvailableDuration(slots1, slots2 [][2]int64, duration int64) []int64 {
	a := append([][2]int64(nil), slots1...)
	b := append([][2]int64(nil), slots2...)
	less := func(s [][2]int64) func(i, j int) bool {
		return func(i, j int) bool {
			if s[i][0] != s[j][0] {
				return s[i][0] < s[j][0]
			}
			return s[i][1] < s[j][1]
		}
	}
	sort.Slice(a, less(a))
	sort.Slice(b, less(b))
	i, j := 0, 0
	for i < len(a) && j < len(b) {
		start := max(a[i][0], b[j][0])
		end := min(a[i][1], b[j][1])
		if end-start >= duration {
			return []int64{start, start + duration}
		}
		if a[i][1] < b[j][1] {
			i++
		} else {
			j++
		}
	}
	return nil
}

func main() {
	seed := int64(1229)
	nextRandom := func() int64 {
		seed = (seed*1103515245 + 12345) % 2147483648
		return seed / 65536
	}
	slots := func(count, width, gap int64) [][2]int64 {
		out := make([][2]int64, 0, count)
		at := nextRandom() % (gap + 1)
		for k := int64(0); k < count; k++ {
			end := at + nextRandom()%width + 1
			out = append(out, [2]int64{at, end})
			at = end + nextRandom()%gap + 1
		}
		for i := len(out) - 1; i >= 1; i-- {
			j := nextRandom() % int64(i+1)
			out[i], out[j] = out[j], out[i]
		}
		return out
	}
	type pair struct{ a, b [][2]int64 }
	pairs := make([]pair, 0, 50)
	for p := 0; p < 50; p++ {
		a := slots(10000, 50000, 50000)
		b := slots(10000, 50000, 50000)
		pairs = append(pairs, pair{a, b})
	}
	check := int64(0)
	for _, p := range pairs {
		for k := int64(1); k <= 10; k++ {
			answer := minAvailableDuration(p.a, p.b, k*4000)
			v := int64(7)
			if len(answer) > 0 {
				v = answer[0]
			}
			check = (check*131 + v) % 1000000007
		}
	}
	fmt.Printf("50 pairs of 10^4 slots, 10 durations: checksum %d\n", check)
}
