// LeetCode 795 — Number of Subarrays with Bounded Maximum: the bench, in
// Go. Mirrors num_subarray_bounded_max.kara: one pass, keeping the last
// place of a number above right and of one in range.
package main

import "fmt"

func numSubarrayBoundedMax(nums []int64, left, right int64) int64 {
	tooBig, inRange := int64(-1), int64(-1)
	var count int64
	for i, x := range nums {
		if x > right {
			tooBig = int64(i)
		} else if x >= left {
			inRange = int64(i)
		}
		if inRange > tooBig {
			count += inRange - tooBig
		}
	}
	return count
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func bigRandom(seed *int64) int64 {
	a := nextRandom(seed)
	b := nextRandom(seed)
	return (a*32768 + b) % 1000000001
}

func main() {
	seed := int64(795)
	arrays := make([][]int64, 16)
	for k := range arrays {
		arrays[k] = make([]int64, 100000)
		for i := range arrays[k] {
			arrays[k][i] = bigRandom(&seed)
		}
	}
	rounds := 8000
	var total, check int64
	for r := 0; r < rounds; r++ {
		a := bigRandom(&seed)
		b := bigRandom(&seed)
		lo, hi := min(a, b), max(a, b)
		count := numSubarrayBoundedMax(arrays[r%16], lo, hi)
		total += count
		check = (check*131 + count%1000000007) % 1000000007
	}
	fmt.Printf("%d rounds of 100000 numbers: %d subarrays, checksum %d\n", rounds, total, check)
}
