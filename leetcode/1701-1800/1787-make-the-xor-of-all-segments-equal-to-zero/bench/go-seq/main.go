// LeetCode #1787: Make the XOR of All Segments Equal to Zero -- the bench in
// Go, mirroring min_changes.kara: a DP over the k groups of positions.
package main

import (
	"fmt"
	"math"
)

func minChanges(nums []int32, k int32) int32 {
	best := make([]int32, 1024)
	for x := range best {
		best[x] = math.MaxInt32 / 2
	}
	best[0] = 0
	for g := int32(0); g < k; g++ {
		count := make(map[int32]int32)
		var size int32
		for i := int(g); i < len(nums); i += int(k) {
			count[nums[i]]++
			size++
		}
		low := best[0]
		for _, b := range best {
			if b < low {
				low = b
			}
		}
		floor := low + size
		next := make([]int32, 1024)
		for x := int32(0); x < 1024; x++ {
			next[x] = floor
			for v, c := range count {
				here := best[x^v] + size - c
				if here < next[x] {
					next[x] = here
				}
			}
		}
		best = next
	}
	return best[0]
}

var seed int64 = 1787

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][]int32, 0, 100)
	for l := 0; l < 100; l++ {
		nums := make([]int32, 0, 600)
		for i := 0; i < 600; i++ {
			nums = append(nums, int32(nextRandom()%1024))
		}
		lists = append(lists, nums)
	}
	var check int64
	for call := int64(0); call < 300; call++ {
		nums := lists[(check+call)%100]
		k := 1 + (check*7+call)%600
		check = (check*31 + int64(minChanges(nums, int32(k)))) % 1000000007
	}
	fmt.Printf("300 calls over 100 lists: checksum %d\n", check)
}
