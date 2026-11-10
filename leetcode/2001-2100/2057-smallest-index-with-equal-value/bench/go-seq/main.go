// LeetCode #2057: Smallest Index With Equal Value -- Go mirror of the ★
// arm's benchmark (equal.kara): the same 1000000 arrays drawn into one
// buffer, each answered by walking its indices from the front.
package main

import "fmt"

var seed int64 = 2057

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func smallestEqual(nums []int64) int64 {
	for i := range nums {
		if int64(i%10) == nums[i] {
			return int64(i)
		}
	}
	return -1
}

func main() {
	nums := make([]int64, 0, 100)
	var found, total, check int64
	for t := 0; t < 1000000; t++ {
		n := nextRandom()%100 + 1
		rare := nextRandom()%20 + 1
		nums = nums[:0]
		for i := int64(0); i < n; i++ {
			d := nextRandom() % 10
			if d == i%10 && nextRandom()%rare != 0 {
				d = (d + 1) % 10
			}
			nums = append(nums, d)
		}
		at := smallestEqual(nums)
		if at >= 0 {
			found++
		}
		total += at
		check = (check*31 + at + 2) % 1000000007
	}
	fmt.Printf("1000000 arrays: %d found, sum %d, checksum %d\n", found, total, check)
}
