// LeetCode #1300 bench: the ★ arm (the numbers sorted and walked from the
// smallest; the best cap is the target's share of what is left, rounded down
// or up) over 50 arrays of 10^4 numbers, up to 20, 100, 1000, 10^4 or 10^5 in
// turn, built once; then 200 passes, each setting one number of every array
// and its target from the checksum so far, answering it, and folding the
// answer into the checksum.
package main

import (
	"fmt"
	"slices"
)

func abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func findBestValue(arr []int64, target int64) int64 {
	sorted := slices.Clone(arr)
	slices.Sort(sorted)
	n := int64(len(sorted))
	var before int64
	for i := int64(0); i < n; i++ {
		left := n - i
		if before+sorted[i]*left >= target {
			x := (target - before) / left
			low := abs(before + x*left - target)
			high := abs(before + (x+1)*left - target)
			if low <= high {
				return x
			}
			return x + 1
		}
		before += sorted[i]
	}
	return sorted[n-1]
}

var seed int64 = 1300

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	tops := []int64{20, 100, 1000, 10000, 100000}
	arrays := [][]int64{}
	for t := 0; t < 50; t++ {
		arr := []int64{}
		for j := 0; j < 10000; j++ {
			hi := nextRandom()
			arr = append(arr, 1+(hi*32768+nextRandom())%tops[t%5])
		}
		arrays = append(arrays, arr)
	}
	var check int64
	for p := int64(0); p < 200; p++ {
		for t, arr := range arrays {
			arr[check%10000] = 1 + check%tops[t%5]
			target := 1 + (check*7919)%100000
			check = (check*31 + findBestValue(arr, target) + p) % 1000000007
		}
	}
	fmt.Printf("200 passes over 50 arrays of 10^4: checksum %d\n", check)
}
