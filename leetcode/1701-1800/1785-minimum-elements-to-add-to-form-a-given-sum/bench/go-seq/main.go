// LeetCode #1785: Minimum Elements to Add to Form a Given Sum -- the bench
// in Go, mirroring min_elements.kara: the gap over the limit, rounded up.
package main

import "fmt"

func minElements(nums []int32, limit int32, goal int32) int32 {
	var sum int64
	for _, x := range nums {
		sum += int64(x)
	}
	gap := int64(goal) - sum
	if gap < 0 {
		gap = -gap
	}
	return int32((gap + int64(limit) - 1) / int64(limit))
}

var seed int64 = 1785

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][]int32, 0, 4000)
	for k := 0; k < 4000; k++ {
		nums := make([]int32, 0, 100)
		for i := 0; i < 100; i++ {
			a := nextRandom()
			b := nextRandom()
			nums = append(nums, int32((a*32768+b)%2000001-1000000))
		}
		lists = append(lists, nums)
	}
	var check int64
	for call := int64(0); call < 6000000; call++ {
		nums := lists[(check+call)%4000]
		limit := 1 + (check+call)%1000000
		goal := check%2000000001 - 1000000000
		check = (check*31 + int64(minElements(nums, int32(limit), int32(goal)))) % 1000000007
	}
	fmt.Printf("6000000 calls over 4000 lists: checksum %d\n", check)
}
