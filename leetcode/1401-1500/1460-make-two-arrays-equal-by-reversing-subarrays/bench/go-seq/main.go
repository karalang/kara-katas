// LeetCode #1460 bench in Go: the ★ arm (both arrays sorted and compared)
// on the same 200 pairs of 1000 values and 50 passes.
package main

import (
	"fmt"
	"slices"
)

func canBeEqual(target, arr []int32) bool {
	a := slices.Clone(target)
	b := slices.Clone(arr)
	slices.Sort(a)
	slices.Sort(b)
	return slices.Equal(a, b)
}

var seed int64 = 1460

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	targets := make([][]int32, 200)
	arrs := make([][]int32, 200)
	for p := 0; p < 200; p++ {
		targets[p] = make([]int32, 1000)
		for k := range targets[p] {
			targets[p][k] = int32(1 + nextRandom()%1000)
		}
		arrs[p] = slices.Clone(targets[p])
		for i := int64(999); i >= 1; i-- {
			j := nextRandom() % (i + 1)
			arrs[p][i], arrs[p][j] = arrs[p][j], arrs[p][i]
		}
	}
	var check int64
	for pass := int64(0); pass < 50; pass++ {
		for p := 0; p < 200; p++ {
			arrs[p][check%1000] = targets[p][(check/7)%1000]
			var same int64
			if canBeEqual(targets[p], arrs[p]) {
				same = 1
			}
			check = (check*31 + same + pass) % 1000000007
		}
	}
	fmt.Printf("50 passes over 200 pairs of 1000 values: checksum %d\n", check)
}
