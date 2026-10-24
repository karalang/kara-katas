// Benchmark: LeetCode #976 Largest Perimeter Triangle -- the ★ arm, sort
// and scan from the top, on 20 lists of 10000 random lengths. Mirrors
// largest_perimeter.kara, .rs, .c and .py.
package main

import (
	"fmt"
	"slices"
)

func largestPerimeter(nums []int64) int64 {
	a := slices.Clone(nums)
	slices.Sort(a)
	for i := len(a) - 1; i >= 2; i-- {
		if a[i-2]+a[i-1] > a[i] {
			return a[i-2] + a[i-1] + a[i]
		}
	}
	return 0
}

var seed int64 = 976

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds, count := 50, 20
	lists := make([][]int64, count)
	for c := range lists {
		lists[c] = make([]int64, 10000)
		for i := range lists[c] {
			hi := nextRandom()
			lists[c][i] = 1 + (hi*32768+nextRandom())%1000000
		}
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			p := largestPerimeter(lists[(r+i)%count])
			total += p
			check = (check*31 + p) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d lists of 10000 lengths: perimeters total %d, checksum %d\n", rounds, count, total, check)
}
