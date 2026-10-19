// LeetCode 805 -- Split Array With Same Average: the bench, mirroring
// split_array.kara with the same sums by size.
package main

import "fmt"

var seed int64 = 805

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func splitArraySameAverage(nums []int64) bool {
	n := int64(len(nums))
	var total int64
	for _, x := range nums {
		total += x
	}
	half := n / 2
	sums := make([]map[int64]struct{}, 0)
	for k := int64(0); k <= half; k++ {
		sums = append(sums, make(map[int64]struct{}))
	}
	sums[0][0] = struct{}{}
	for _, x := range nums {
		for k := half; k >= 1; k-- {
			before := make([]int64, 0, len(sums[k-1]))
			for s := range sums[k-1] {
				before = append(before, s)
			}
			for _, s := range before {
				sums[k][s+x] = struct{}{}
			}
		}
	}
	for k := int64(1); k <= half; k++ {
		if total*k%n == 0 {
			if _, ok := sums[k][total*k/n]; ok {
				return true
			}
		}
	}
	return false
}

func main() {
	arrays := make([][]int64, 0)
	for a := 0; a < 16; a++ {
		nums := make([]int64, 0)
		var sum int64
		for i := 0; i < 29; i++ {
			x := nextRandom() % 300
			nums = append(nums, x)
			sum += x
		}
		var last int64
		if a%2 == 0 {
			last = nextRandom() % 300
		} else {
			last = (31-sum%30)%30 + 30*(nextRandom()%9)
		}
		nums = append(nums, last)
		arrays = append(arrays, nums)
	}
	var rounds int64 = 400
	yes := 0
	var check int64
	for r := int64(0); r < rounds; r++ {
		can := splitArraySameAverage(arrays[r%16])
		v := int64(2)
		if can {
			yes++
			v = 1
		}
		check = (check*131 + v) % 1000000007
	}
	fmt.Printf("%d rounds of 30 numbers: %d can be split, checksum %d\n", rounds, yes, check)
}
