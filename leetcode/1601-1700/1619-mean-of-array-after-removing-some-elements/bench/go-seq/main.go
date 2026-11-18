// LeetCode #1619: Mean of Array After Removing Some Elements -- the bench in
// Go, mirroring trim.kara: sort a copy, then the mean of the middle 90%.
package main

import (
	"fmt"
	"math"
	"slices"
)

func trimMean(arr []int32) float64 {
	sorted := slices.Clone(arr)
	slices.Sort(sorted)
	k := len(sorted) / 20
	kept := sorted[k : len(sorted)-k]
	var sum int64
	for _, x := range kept {
		sum += int64(x)
	}
	return float64(sum) / float64(len(kept))
}

var seed int64 = 1619

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int32, 20000)
	for a := range arrays {
		arr := make([]int32, 1000)
		for i := range arr {
			hi := nextRandom()
			lo := nextRandom()
			arr[i] = int32((hi*32768 + lo) % 100001)
		}
		arrays[a] = arr
	}
	var check int64
	total := 0.0
	for _, arr := range arrays {
		mean := trimMean(arr)
		total += mean
		check = (check*31 + int64(math.Round(mean*100000.0)) + 1) % 1000000007
	}
	fmt.Printf("20000 arrays of 1000 values: means sum to %.5f, checksum %d\n", total, check)
}
