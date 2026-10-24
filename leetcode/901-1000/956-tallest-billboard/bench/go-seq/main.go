// LeetCode #956: Tallest Billboard -- Go mirror of the Kara bench program
// (the shorter side by difference).
package main

import "fmt"

func tallestBillboard(rods []int64) int64 {
	total := int64(0)
	for _, r := range rods {
		total += r
	}
	best := make([]int64, total+1)
	prev := make([]int64, total+1)
	for d := range best {
		best[d] = -1
	}
	best[0] = 0
	for _, r := range rods {
		copy(prev, best)
		for d := int64(0); d <= total; d++ {
			short := prev[d]
			if short < 0 {
				continue
			}
			if d+r <= total && short > best[d+r] {
				best[d+r] = short
			}
			nd := d - r
			if nd < 0 {
				nd = -nd
			}
			m := r
			if d < r {
				m = d
			}
			ns := short + m
			if ns > best[nd] {
				best[nd] = ns
			}
		}
	}
	return best[0]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	rounds, count, n := 30, 200, 20
	seed := int64(956)
	sets := [][]int64{}
	for s := 0; s < count; s++ {
		rods := make([]int64, n)
		for i := range rods {
			rods[i] = 1 + nextRandom(&seed)%250
		}
		sets = append(sets, rods)
	}
	total, check := int64(0), int64(0)
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			k := (r + i) % count
			h := tallestBillboard(sets[k])
			total += h
			check = (check*31 + h) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d sets of %d rods up to 250: heights adding to %d, checksum %d\n", rounds, count, n, total, check)
}
