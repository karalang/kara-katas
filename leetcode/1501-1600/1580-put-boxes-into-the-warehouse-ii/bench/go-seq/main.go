// LeetCode #1580 bench: the same usable heights matched smallest first, in
// Go.
package main

import (
	"fmt"
	"slices"
)

func maxBoxesInWarehouse(boxes, warehouse []int64) int64 {
	m := len(warehouse)
	fromLeft := slices.Clone(warehouse)
	for i := 1; i < m; i++ {
		fromLeft[i] = min(fromLeft[i], fromLeft[i-1])
	}
	usable := slices.Clone(warehouse)
	for i := m - 2; i >= 0; i-- {
		usable[i] = min(usable[i], usable[i+1])
	}
	for i := 0; i < m; i++ {
		usable[i] = max(usable[i], fromLeft[i])
	}
	slices.Sort(usable)
	sorted := slices.Clone(boxes)
	slices.Sort(sorted)
	placed := 0
	for _, room := range usable {
		if placed < len(sorted) && sorted[placed] <= room {
			placed++
		}
	}
	return int64(placed)
}

var seed int64 = 1580

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	type problem struct{ boxes, warehouse []int64 }
	problems := make([]problem, 0, 40)
	for p := 0; p < 40; p++ {
		boxes := make([]int64, 0, 100000)
		for i := 0; i < 100000; i++ {
			boxes = append(boxes, (nextRandom()*32768+nextRandom())%1000000000+1)
		}
		warehouse := make([]int64, 0, 100000)
		for i := int64(0); i < 100000; i++ {
			d := i - 50000
			if d < 0 {
				d = -d
			}
			warehouse = append(warehouse, d*20000+(nextRandom()*32768+nextRandom())%1000000)
		}
		problems = append(problems, problem{boxes, warehouse})
	}
	var check, total int64
	for _, pr := range problems {
		placed := maxBoxesInWarehouse(pr.boxes, pr.warehouse)
		total += placed
		check = mix(check, placed)
	}
	fmt.Printf("40 problems of 100000 boxes and rooms: boxes placed %d, checksum %d\n", total, check)
}
