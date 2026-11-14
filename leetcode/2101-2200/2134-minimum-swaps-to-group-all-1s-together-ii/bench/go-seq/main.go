// LeetCode #2134: Minimum Swaps to Group All 1's Together II -- the
// benchmark, the same algorithm as swaps.kara.
package main

import "fmt"

func minSwaps(nums []int64) int64 {
	n := int64(len(nums))
	k := int64(0)
	for _, v := range nums {
		k += v
	}
	inside := int64(0)
	for i := int64(0); i < k; i++ {
		inside += nums[i]
	}
	most := inside
	for i := k; i < n+k; i++ {
		inside += nums[i%n] - nums[(i-k)%n]
		if inside > most {
			most = inside
		}
	}
	return k - most
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(2134)
	arrays := make([][]int64, 20)
	for a := int64(0); a < 20; a++ {
		arrays[a] = make([]int64, 100000)
		for i := range arrays[a] {
			if nextRandom(&seed)%(a+2) == 0 {
				arrays[a][i] = 1
			}
		}
	}
	total, check := int64(0), int64(0)
	for round := int64(0); round < 10; round++ {
		for a := 0; a < 20; a++ {
			hi := nextRandom(&seed)
			at := (hi*32768 + nextRandom(&seed)) % 100000
			arrays[a][at] = 1 - arrays[a][at]
			swaps := minSwaps(arrays[a])
			total += swaps
			check = (check*31 + swaps + round) % 1000000007
		}
	}
	fmt.Printf("200 solves: %d swaps in all, checksum %d\n", total, check)
}
