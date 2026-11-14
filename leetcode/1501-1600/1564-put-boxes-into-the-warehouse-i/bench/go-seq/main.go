// LeetCode #1564: Put Boxes Into the Warehouse I -- bench: the ★ arm
// (usable heights, the smallest boxes into the deepest rooms) over 20
// problems of 100000 boxes and 100000 rooms, built once, each asked 10
// times.
// Go mirror of warehouse.kara; the boxes' copy is sorted by slices.Sort.
package main

import (
	"fmt"
	"slices"
)

func maxBoxesInWarehouse(boxes, warehouse []int64) int64 {
	usable := slices.Clone(warehouse)
	for i := 1; i < len(usable); i++ {
		usable[i] = min(usable[i], usable[i-1])
	}
	sorted := slices.Clone(boxes)
	slices.Sort(sorted)
	placed := 0
	for r := len(usable) - 1; r >= 0; r-- {
		if placed < len(sorted) && sorted[placed] <= usable[r] {
			placed++
		}
	}
	return int64(placed)
}

var seed int64 = 1564

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

type problem struct{ boxes, warehouse []int64 }

func main() {
	const top = int64(1000000000)
	problems := make([]problem, 20)
	for p := range problems {
		boxes := make([]int64, 100000)
		for i := range boxes {
			v := nextRandom() * 32768
			boxes[i] = (v+nextRandom())%top + 1
		}
		warehouse := make([]int64, 100000)
		for i := range warehouse {
			v := nextRandom() * 32768
			warehouse[i] = top - (v+nextRandom())%((top+1)/2)
		}
		problems[p] = problem{boxes, warehouse}
	}
	var check, total int64
	for pass := 0; pass < 10; pass++ {
		for _, pr := range problems {
			placed := maxBoxesInWarehouse(pr.boxes, pr.warehouse)
			total += placed
			check = mix(check, placed)
		}
	}
	fmt.Printf("10 passes over 20 problems of 100000 boxes and rooms: %d boxes, checksum %d\n", total, check)
}
