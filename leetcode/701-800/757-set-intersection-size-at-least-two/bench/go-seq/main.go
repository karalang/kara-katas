// LeetCode 757 — Set Intersection Size At Least Two: benchmark, the ★ arm in Go.
package main

import (
	"fmt"
	"sort"
)

func intersectionSizeTwo(intervals [][]int64) int64 {
	order := make([][]int64, len(intervals))
	copy(order, intervals)
	sort.Slice(order, func(i, j int) bool {
		if order[i][1] != order[j][1] {
			return order[i][1] < order[j][1]
		}
		return order[i][0] > order[j][0]
	})
	count := int64(0)
	second := int64(-1)
	largest := int64(-1)
	for _, interval := range order {
		start, end := interval[0], interval[1]
		if start > largest {
			count += 2
			second = end - 1
			largest = end
		} else if start > second {
			count++
			second = largest
			largest = end
		}
	}
	return count
}

var seed int64 = 757

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := int64(2000)
	total := int64(0)
	check := int64(0)
	for r := int64(0); r < rounds; r++ {
		intervals := [][]int64{}
		for i := 0; i < 3000; i++ {
			width := 1 + nextRandom()%100000
			a := nextRandom() * 32768 % (100000000 - width + 1)
			intervals = append(intervals, []int64{a, a + width})
		}
		answer := intersectionSizeTwo(intervals)
		total += answer
		check = (check*31 + answer) % 1000000007
	}
	fmt.Printf("%d sets of 3000 intervals: %d points in all, checksum %d\n", rounds, total, check)
}
