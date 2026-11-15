// LeetCode #1577: Number of Ways Where Square of Number Is Equal to
// Product of Two Numbers -- bench: the ★ arm (a walk with a Map of the
// values seen) over 10 pairs of arrays of 1000 values, each a power of 2
// or 3 times a factor below 100, drawn first.
package main

import "fmt"

func ways(squares, products []int64) int64 {
	var total int64
	for _, x := range squares {
		target := x * x
		seen := make(map[int64]int64)
		for _, y := range products {
			if target%y == 0 {
				total += seen[target/y]
			}
			seen[y]++
		}
	}
	return total
}

func numTriplets(nums1, nums2 []int64) int64 {
	return ways(nums1, nums2) + ways(nums2, nums1)
}

var seed int64 = 1577

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	arrays := make([][]int64, 0, 20)
	for a := 0; a < 20; a++ {
		nums := make([]int64, 0, 1000)
		for i := 0; i < 1000; i++ {
			v := nextRandom()%100 + 1
			times := nextRandom() % 4
			for t := int64(0); t < times; t++ {
				v *= 2 + nextRandom()%2
			}
			nums = append(nums, min(v, 100000))
		}
		arrays = append(arrays, nums)
	}
	var check, total int64
	for p := 0; p < 10; p++ {
		w := numTriplets(arrays[2*p], arrays[2*p+1])
		total += w
		check = mix(check, w)
	}
	fmt.Printf("10 pairs of arrays of 1000 values: triplets total %d, checksum %d\n", total, check)
}
