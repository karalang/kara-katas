// LeetCode #2248: Intersection of Multiple Arrays -- the benchmark's Go
// mirror of common.kara: a count for every value from 1 to 1000, kept
// where it reaches the number of arrays.
package main

import "fmt"

func intersection(nums [][]int64) []int64 {
	count := make([]int64, 1001)
	for _, row := range nums {
		for _, v := range row {
			count[v]++
		}
	}
	common := []int64{}
	for v := int64(1); v <= 1000; v++ {
		if count[v] == int64(len(nums)) {
			common = append(common, v)
		}
	}
	return common
}

var seed int64 = 2248

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	check := int64(0)
	pool := make([]int64, 150)
	for i := range pool {
		pool[i] = int64(i + 1)
	}
	for t := 0; t < 20000; t++ {
		nums := make([][]int64, 0, 10)
		for r := 0; r < 10; r++ {
			for i := 0; i < 100; i++ {
				j := i + int(nextRandom()%int64(150-i))
				pool[i], pool[j] = pool[j], pool[i]
			}
			row := make([]int64, 100)
			copy(row, pool[:100])
			nums = append(nums, row)
		}
		common := intersection(nums)
		acc := int64(len(common))
		for _, v := range common {
			acc = (acc*1009 + v) % 1000000007
		}
		check = (check*31 + acc) % 1000000007
	}
	fmt.Printf("20000 cases: checksum %d\n", check)
}
