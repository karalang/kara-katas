// LeetCode #2149: Rearrange Array Elements by Sign -- the benchmark's Go
// mirror of signs.kara.
package main

import "fmt"

func rearrangeArray(nums []int64) []int64 {
	out := make([]int64, len(nums))
	positive, negative := 0, 1
	for _, x := range nums {
		if x > 0 {
			out[positive] = x
			positive += 2
		} else {
			out[negative] = x
			negative += 2
		}
	}
	return out
}

var seed int64 = 2149

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	hi := nextRandom()
	return hi*32768 + nextRandom()
}

func main() {
	const n = 200000
	lists := [][]int64{}
	for l := 0; l < 4; l++ {
		nums := make([]int64, 0, n)
		for i := int64(0); i < n; i++ {
			size := nextRandom()%100000 + 1
			if i < n/2 {
				nums = append(nums, size)
			} else {
				nums = append(nums, -size)
			}
		}
		for i := int64(n - 1); i > 0; i-- {
			j := wide() % (i + 1)
			nums[i], nums[j] = nums[j], nums[i]
		}
		lists = append(lists, nums)
	}
	var check int64
	for round := int64(0); round < 25; round++ {
		for l := 0; l < 4; l++ {
			a := wide() % n
			b := wide() % n
			lists[l][a], lists[l][b] = lists[l][b], lists[l][a]
			out := rearrangeArray(lists[l])
			at := wide() % n
			check = (check*31 + out[0] + out[n-1] + out[at] + 300000 + round) % 1000000007
		}
	}
	fmt.Printf("100 answers: checksum %d\n", check)
}
