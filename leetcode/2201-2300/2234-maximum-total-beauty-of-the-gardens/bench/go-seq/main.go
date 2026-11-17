// LeetCode #2234: Maximum Total Beauty of the Gardens -- the benchmark's
// Go mirror of beauty.kara: every split of complete gardens tried, the
// level of the rest by a binary search on the level.
package main

import (
	"fmt"
	"sort"
)

func maximumBeauty(flowers []int64, newFlowers, target, full, partial int64) int64 {
	n := int64(len(flowers))
	sorted := make([]int64, n)
	for i, f := range flowers {
		if f < target {
			sorted[i] = f
		} else {
			sorted[i] = target
		}
	}
	sort.Slice(sorted, func(i, j int) bool { return sorted[i] < sorted[j] })
	prefix := make([]int64, n+1)
	for i := int64(0); i < n; i++ {
		prefix[i+1] = prefix[i] + sorted[i]
	}
	best, cost := int64(0), int64(0)
	for c := n; c >= 0; c-- {
		if c < n {
			cost += target - sorted[c]
		}
		if cost > newFlowers {
			break
		}
		complete := (n - c) * full
		if c == 0 {
			if complete > best {
				best = complete
			}
		} else if sorted[c-1] < target {
			left := newFlowers - cost
			low, high := sorted[0], target-1
			for low < high {
				m := (low + high + 1) / 2
				a, b := int64(0), c
				for a < b {
					mid := (a + b) / 2
					if sorted[mid] < m {
						a = mid + 1
					} else {
						b = mid
					}
				}
				if m*a-prefix[a] <= left {
					low = m
				} else {
					high = m - 1
				}
			}
			if complete+low*partial > best {
				best = complete + low*partial
			}
		}
	}
	return best
}

var seed int64 = 2234

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	flowers := make([]int64, 20000)
	for i := range flowers {
		flowers[i] = wideRandom()%100000 + 1
	}
	check := int64(0)
	for pass := 0; pass < 20; pass++ {
		// punch: one garden drawn again before each pass, and the new
		// flowers drawn anew
		at := nextRandom() % 20000
		flowers[at] = wideRandom()%100000 + 1
		newFlowers := wideRandom()%1200000000 + 1
		check = (check*31 + maximumBeauty(flowers, newFlowers, 100000, 100000, 100000)) % 1000000007
	}
	fmt.Printf("20 passes over 20000 gardens: checksum %d\n", check)
}
