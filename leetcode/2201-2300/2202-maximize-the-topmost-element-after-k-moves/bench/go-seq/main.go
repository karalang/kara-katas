// benchmark's Go mirror of top.kara (LeetCode #2202, the ★ arm): the first
// k - 1 numbers and the one at index k.
package main

import "fmt"

func maximumTop(nums []int64, k int64) int64 {
	n := int64(len(nums))
	if n == 1 {
		if k%2 == 1 {
			return -1
		}
		return nums[0]
	}
	best := int64(-1)
	reach := k - 1
	if n < reach {
		reach = n
	}
	for i := int64(0); i < reach; i++ {
		if nums[i] > best {
			best = nums[i]
		}
	}
	if k < n && nums[k] > best {
		best = nums[k]
	}
	return best
}

var seed int64 = 2202

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	hi := nextRandom()
	return hi*32768 + nextRandom()
}

func main() {
	piles := [][]int64{}
	ks := [][]int64{}
	for p := 0; p < 10; p++ {
		nums := make([]int64, 100000)
		for i := range nums {
			nums[i] = wideRandom() % 1000000001
		}
		piles = append(piles, nums)
		k := make([]int64, 10)
		for j := range k {
			k[j] = wideRandom() % 100002
		}
		ks = append(ks, k)
	}
	var check int64
	for pass := 0; pass < 50; pass++ {
		for p := 0; p < 10; p++ {
			for _, k := range ks[p] {
				check = (check*31 + maximumTop(piles[p], k) + 1) % 1000000007
			}
		}
	}
	fmt.Printf("50 passes over 10 piles: checksum %d\n", check)
}
