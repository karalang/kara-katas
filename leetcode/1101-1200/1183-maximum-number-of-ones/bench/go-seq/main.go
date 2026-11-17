// LeetCode #1183: Maximum Number of Ones -- the ★ arm in Go: the cells on
// each position of the `side * side` square counted, sorted largest first,
// and the first `max_ones` summed.
package main

import (
	"fmt"
	"sort"
)

func maximumNumberOfOnes(width, height, sideLength, maxOnes int64) int64 {
	counts := []int64{}
	for i := int64(0); i < sideLength; i++ {
		for j := int64(0); j < sideLength; j++ {
			across := (width-i-1)/sideLength + 1
			down := (height-j-1)/sideLength + 1
			counts = append(counts, across*down)
		}
	}
	sort.Slice(counts, func(a, b int) bool { return counts[a] > counts[b] })
	total := int64(0)
	for _, c := range counts[:maxOnes] {
		total += c
	}
	return total
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1183)
	cases := [][4]int64{}
	for k := 0; k < 1000; k++ {
		width := 1 + nextRandom(&seed)%100
		height := 1 + nextRandom(&seed)%100
		side := 1 + nextRandom(&seed)%min(width, height)
		maxOnes := nextRandom(&seed) % (side*side + 1)
		cases = append(cases, [4]int64{width, height, side, maxOnes})
	}
	rounds := 100
	check := int64(0)
	for r := 0; r < rounds; r++ {
		for _, c := range cases {
			check = (check*131 + maximumNumberOfOnes(c[0], c[1], c[2], c[3]) + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d rounds of 1000 cases: checksum %d\n", rounds, check)
}
