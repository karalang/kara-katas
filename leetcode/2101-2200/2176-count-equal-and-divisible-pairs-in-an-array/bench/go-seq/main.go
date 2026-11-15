// LeetCode #2176: Count Equal and Divisible Pairs in an Array -- the
// benchmark's Go mirror of pairs.kara.
package main

import "fmt"

func countPairs(nums []int64, k int64) int64 {
	n := int64(len(nums))
	var pairs int64
	for i := int64(0); i < n; i++ {
		for j := i + 1; j < n; j++ {
			if nums[i] == nums[j] && i*j%k == 0 {
				pairs++
			}
		}
	}
	return pairs
}

var seed int64 = 2176

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	row := make([]int64, 0, 100000)
	for i := 0; i < 100000; i++ {
		row = append(row, nextRandom()%5+1)
	}
	var check int64
	for r := 0; r < 20000; r++ {
		start := nextRandom() % 99901
		k := nextRandom()%100 + 1
		pairs := countPairs(row[start:start+100], k)
		check = (check*31 + pairs) % 1000000007
	}
	fmt.Printf("20000 solves: checksum %d\n", check)
}
