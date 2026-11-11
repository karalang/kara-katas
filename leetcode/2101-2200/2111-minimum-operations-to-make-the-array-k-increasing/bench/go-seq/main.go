// LeetCode #2111: Minimum Operations to Make the Array K-Increasing -- the
// benchmark, the same algorithm as increasing.kara: each chain's patience
// tails, the first tail above each value found by binary search.

package main

import "fmt"

func kIncreasing(arr []int64, k int) int64 {
	var changes int64
	for r := 0; r < k; r++ {
		tails := []int64{}
		var length int64
		for i := r; i < len(arr); i += k {
			x := arr[i]
			lo, hi := 0, len(tails)
			for lo < hi {
				mid := lo + (hi-lo)/2
				if tails[mid] <= x {
					lo = mid + 1
				} else {
					hi = mid
				}
			}
			if lo == len(tails) {
				tails = append(tails, x)
			} else {
				tails[lo] = x
			}
			length++
		}
		changes += length - int64(len(tails))
	}
	return changes
}

var seed int64 = 2111

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int64, 10)
	for a := range arrays {
		arr := make([]int64, 100000)
		for i := range arr {
			hi := nextRandom()
			lo := nextRandom()
			arr[i] = (hi*32768+lo)%100000 + 1
		}
		arrays[a] = arr
	}
	var total, check int64
	for round := 0; round < 10; round++ {
		for a := 0; a < 10; a++ {
			at := round*9973 + a
			arrays[a][at] = arrays[a][at]%100000 + 1
			got := kIncreasing(arrays[a], round+1)
			total += got
			check = (check*31 + got) % 1000000007
		}
	}
	fmt.Printf("100 solves: %d operations, checksum %d\n", total, check)
}
