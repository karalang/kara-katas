// LeetCode 755 — Pour Water, bench: the ★ arm (one drop at a time),
// mirrored from pour_water.kara.
package main

import "fmt"

func pourWater(heights []int64, volume, k int64) []int64 {
	h := make([]int64, len(heights))
	copy(h, heights)
	n := int64(len(h))
	for v := int64(0); v < volume; v++ {
		best := k
		for _, d := range [2]int64{-1, 1} {
			i := k
			for i+d >= 0 && i+d < n && h[i+d] <= h[i] {
				if h[i+d] < h[best] {
					best = i + d
				}
				i += d
			}
			if best != k {
				break
			}
		}
		h[best]++
	}
	return h
}

var seed int64 = 755

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := int64(6000)
	var water, check int64
	for r := int64(0); r < rounds; r++ {
		heights := make([]int64, 0, 100)
		for i := 0; i < 100; i++ {
			heights = append(heights, nextRandom()%100)
		}
		volume := int64(2000)
		k := nextRandom() % 100
		after := pourWater(heights, volume, k)
		for _, x := range after {
			water += x
			check = (check*31 + x) % 1000000007
		}
	}
	fmt.Printf("%d landscapes of 100 columns, 2000 drops each: %d units in all, checksum %d\n", rounds, water, check)
}
