// LeetCode #1228 bench: the ★ arm in Go, over the same 2000 random
// progressions and 2000 passes as the Kāra bench.
package main

import "fmt"

func missingNumber(arr []int64) int64 {
	n := int64(len(arr))
	step := (arr[n-1] - arr[0]) / n
	lo, hi := int64(0), n-1
	for lo < hi {
		mid := (lo + hi) / 2
		if arr[mid] == arr[0]+mid*step {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	return arr[0] + lo*step
}

func main() {
	seed := int64(1228)
	nextRandom := func() int64 {
		seed = (seed*1103515245 + 12345) % 2147483648
		return seed / 65536
	}
	arrays := make([][]int64, 0, 2000)
	for a := 0; a < 2000; a++ {
		first := nextRandom() % 100001
		low := -(first / 1000)
		high := (100000 - first) / 1000
		step := low + nextRandom()%(high-low+1)
		gone := nextRandom()%999 + 1
		arr := make([]int64, 0, 1000)
		for i := int64(0); i < 1001; i++ {
			if i != gone {
				arr = append(arr, first+i*step)
			}
		}
		arrays = append(arrays, arr)
	}
	check := int64(0)
	for pass := 0; pass < 2000; pass++ {
		for _, arr := range arrays {
			check = (check*131 + missingNumber(arr)) % 1000000007
		}
	}
	fmt.Printf("2000 progressions of 1000 values, 2000 passes: checksum %d\n", check)
}
