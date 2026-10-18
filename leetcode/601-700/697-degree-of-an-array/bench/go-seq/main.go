// LeetCode #697: Degree of an Array -- bench program, Go mirror of the table arm.
package main

import "fmt"

var seed int64 = 697

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func findShortestSubArray(nums []int64) int64 {
	const size = 50000
	count := make([]int64, size)
	first := make([]int64, size)
	last := make([]int64, size)
	for x := range first {
		first[x] = -1
	}
	for i, x := range nums {
		if first[x] < 0 {
			first[x] = int64(i)
		}
		last[x] = int64(i)
		count[x]++
	}
	var degree int64
	best := int64(len(nums))
	for x := 0; x < size; x++ {
		if count[x] == 0 {
			continue
		}
		span := last[x] - first[x] + 1
		if count[x] > degree || (count[x] == degree && span < best) {
			degree = count[x]
			best = span
		}
	}
	return best
}

func main() {
	arrays := [][]int64{}
	for k := int64(0); k < 40; k++ {
		rng := 1 + 1250*k
		nums := make([]int64, 0, 50000)
		for i := 0; i < 50000; i++ {
			a := nextRandom()
			b := nextRandom()
			nums = append(nums, (a*65536+b)%rng)
		}
		arrays = append(arrays, nums)
	}
	rounds := 20
	var total, checksum int64
	for r := 0; r < rounds; r++ {
		for _, nums := range arrays {
			c := findShortestSubArray(nums)
			total += c
			checksum = (checksum*31 + c) % 1000000007
		}
	}
	fmt.Printf("%d rounds of 40 arrays of 50000: shortest spans sum to %d, checksum %d\n", rounds, total, checksum)
}
