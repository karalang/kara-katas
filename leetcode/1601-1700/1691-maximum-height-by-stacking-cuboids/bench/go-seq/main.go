// LeetCode #1691: Maximum Height by Stacking Cuboids -- the bench's Go
// mirror: the ★ arm on 3000 random sets of 100 cuboids, all drawn first,
// each answered 5 times.
package main

import (
	"fmt"
	"slices"
)

func maxHeight(cuboids [][]int32) int32 {
	boxes := make([][]int32, len(cuboids))
	for i, c := range cuboids {
		sides := slices.Clone(c)
		slices.Sort(sides)
		boxes[i] = sides
	}
	slices.SortFunc(boxes, slices.Compare[[]int32])
	n := len(boxes)
	best := make([]int32, n)
	var tallest int32
	for i := 0; i < n; i++ {
		best[i] = boxes[i][2]
		for j := 0; j < i; j++ {
			if boxes[j][0] <= boxes[i][0] && boxes[j][1] <= boxes[i][1] && boxes[j][2] <= boxes[i][2] {
				best[i] = max(best[i], best[j]+boxes[i][2])
			}
		}
		tallest = max(tallest, best[i])
	}
	return tallest
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1691

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, size, rounds = 3000, 100, 5
	sets := make([][][]int32, count)
	for c := range sets {
		sets[c] = make([][]int32, size)
		for i := range sets[c] {
			sides := make([]int32, 3)
			for d := range sides {
				sides[d] = int32(nextRandom()%100 + 1)
			}
			sets[c][i] = sides
		}
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, cuboids := range sets {
			answer := int64(maxHeight(cuboids))
			total += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d sets of %d cuboids, %d rounds: answers sum to %d, checksum %d\n", count, size, rounds, total, check)
}
