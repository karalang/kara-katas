// Benchmark for #658: binary search for the window, as the Kara ★ arm.
package main

import (
	"fmt"
	"sort"
)

func findClosestElements(arr []int64, k, x int64) []int64 {
	low, high := int64(0), int64(len(arr))-k
	for low < high {
		middle := (low + high) / 2
		if x-arr[middle] > arr[middle+k]-x {
			low = middle + 1
		} else {
			high = middle
		}
	}
	out := make([]int64, k)
	copy(out, arr[low:low+k])
	return out
}

var seed int64 = 658

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	n, queries := int64(1000000), int64(1000000)
	arr := make([]int64, n)
	for i := range arr {
		hi := nextRandom()
		lo := nextRandom()
		arr[i] = (hi*32768+lo)%2000001 - 1000000
	}
	sort.Slice(arr, func(i, j int) bool { return arr[i] < arr[j] })
	var checksum int64
	for q := int64(0); q < queries; q++ {
		k := 1 + q%64
		hi := nextRandom()
		lo := nextRandom()
		x := (hi*32768+lo)%2200001 - 1100000
		got := findClosestElements(arr, k, x)
		checksum = (checksum*31 + got[0]*3 + got[len(got)-1]*5 + int64(len(got)) + 10000000) % 1000000007
	}
	fmt.Printf("%d numbers, %d queries: checksum %d\n", n, queries, checksum)
}
