// Benchmark for #475: Go mirror of the ★ arm (sort the heaters, binary
// search per house); see ../heaters.kara.
package main

import (
	"fmt"
	"math"
	"sort"
)

func firstAtOrAfter(heaters []int64, x int64) int {
	lo := 0
	hi := len(heaters)
	for lo < hi {
		mid := lo + (hi-lo)/2
		if heaters[mid] < x {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	return lo
}

func findRadius(houses, heaters []int64) int64 {
	sorted := append([]int64(nil), heaters...)
	sort.Slice(sorted, func(a, b int) bool { return sorted[a] < sorted[b] })
	var radius int64
	for _, house := range houses {
		at := firstAtOrAfter(sorted, house)
		var nearest int64 = math.MaxInt64
		if at < len(sorted) {
			nearest = sorted[at] - house
		}
		if at > 0 && house-sorted[at-1] < nearest {
			nearest = house - sorted[at-1]
		}
		if nearest > radius {
			radius = nearest
		}
	}
	return radius
}

var seed int64 = 475

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	houses := make([]int64, 0, 30000)
	for i := 0; i < 30000; i++ {
		a := nextRandom()
		b := nextRandom()
		houses = append(houses, 1+(a*32768+b)%1000000000)
	}
	rounds := 200
	var total, checksum int64
	for r := 0; r < rounds; r++ {
		heaters := make([]int64, 0, 30000)
		for i := 0; i < 30000; i++ {
			a := nextRandom()
			b := nextRandom()
			heaters = append(heaters, 1+(a*32768+b)%1000000000)
		}
		got := findRadius(houses, heaters)
		total += got
		checksum = (checksum*31 + got) % 1000000007
	}
	fmt.Printf("%d rounds of 30000 houses and 30000 heaters: radii add up to %d, checksum %d\n", rounds, total, checksum)
}
