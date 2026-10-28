// Benchmark: LeetCode #1005 Maximize Sum Of Array After K Negations -- the
// ★ arm, counting, on arrays of 10000 numbers, LeetCode's longest.
// Mirrors largest_sum.kara, .c, .rs and .py.
package main

import "fmt"

func largestSumAfterKNegations(nums []int64, k int64) int64 {
	count := make([]int64, 201)
	for _, x := range nums {
		count[x+100]++
	}
	left := k
	v := int64(-100)
	for v < 0 && left > 0 {
		flip := count[v+100]
		if left < flip {
			flip = left
		}
		count[v+100] -= flip
		count[100-v] += flip
		left -= flip
		v++
	}
	sum := int64(0)
	for v := int64(-100); v < 101; v++ {
		sum += v * count[v+100]
	}
	if left%2 == 1 {
		smallest := int64(0)
		for count[smallest+100] == 0 {
			smallest++
		}
		sum -= 2 * smallest
	}
	return sum
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	rounds := int64(2500)
	n := int64(10000)
	seed := int64(1005)
	arrays := make([][]int64, 0, 20)
	for t := int64(0); t < 20; t++ {
		nums := make([]int64, 0, n)
		for j := int64(0); j < n; j++ {
			size := nextRandom(&seed) % 101
			if nextRandom(&seed)%8 < t%7+1 {
				nums = append(nums, -size)
			} else {
				nums = append(nums, size)
			}
		}
		arrays = append(arrays, nums)
	}
	total := int64(0)
	check := int64(0)
	for r := int64(0); r < rounds; r++ {
		for i := int64(0); i < 20; i++ {
			t := (r + i) % 20
			k := 1 + (r*37+t*101)%10000
			got := largestSumAfterKNegations(arrays[t], k)
			total += got
			check = (check*31 + got%1000000007 + 1000000007) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 20 arrays of %d numbers: answers sum to %d, checksum %d\n", rounds, n, total, check)
}
