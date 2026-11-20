// LeetCode #2261: K Divisible Elements Subarrays -- Go mirror of the ★
// arm: from every start the subarray grows until more than k of its
// elements are divisible by p, each one put into a set. Go's maps cannot
// key on a slice, so each subarray is keyed by its elements written into
// a string, eight bytes apiece. Same workload and checksum as
// divisible.kara.
package main

import (
	"encoding/binary"
	"fmt"
)

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func countDistinct(nums []int64, k, p int64) int64 {
	seen := map[string]struct{}{}
	for start := range nums {
		divisible := int64(0)
		run := []byte{}
		for end := start; end < len(nums); end++ {
			if nums[end]%p == 0 {
				divisible++
			}
			if divisible > k {
				break
			}
			run = binary.LittleEndian.AppendUint64(run, uint64(nums[end]))
			seen[string(run)] = struct{}{}
		}
	}
	return int64(len(seen))
}

func main() {
	seed := int64(2261)
	check := int64(0)
	for t := 0; t < 40; t++ {
		nums := make([]int64, 200)
		for i := range nums {
			nums[i] = nextRandom(&seed)%200 + 1
		}
		p := nextRandom(&seed)%8 + 2
		k := nextRandom(&seed)%196 + 5
		check = (check*31 + countDistinct(nums, k, p)) % 1000000007
	}
	fmt.Printf("40 arrays of 200: checksum %d\n", check)
}
