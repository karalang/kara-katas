// LeetCode #2229: Check if an Array Is Consecutive -- the benchmark's Go
// mirror of consecutive.kara: the span against the count, and a map to
// find a repeat.
package main

import "fmt"

func isConsecutive(nums []int64) bool {
	seen := map[int64]bool{}
	smallest, largest := nums[0], nums[0]
	for _, x := range nums {
		if seen[x] {
			return false
		}
		seen[x] = true
		smallest = min(smallest, x)
		largest = max(largest, x)
	}
	return largest-smallest+1 == int64(len(nums))
}

var seed int64 = 2229

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	lists := make([][]int64, 4)
	for l := range lists {
		nums := make([]int64, 100000)
		for i := range nums {
			nums[i] = int64(i)
		}
		for i := int64(99999); i >= 1; i-- {
			j := wideRandom() % (i + 1)
			nums[i], nums[j] = nums[j], nums[i]
		}
		if l >= 2 {
			from := wideRandom() % 100000
			to := wideRandom() % 100000
			nums[to] = nums[from]
		}
		lists[l] = nums
	}
	yes := 0
	var check int64
	for r := 0; r < 25; r++ {
		for l := 0; l < 4; l++ {
			// punch: two numbers trade places before each answer
			i := wideRandom() % 100000
			j := wideRandom() % 100000
			lists[l][i], lists[l][j] = lists[l][j], lists[l][i]
			answer := isConsecutive(lists[l])
			if answer {
				yes++
			}
			add := int64(2)
			if answer {
				add = 1
			}
			check = (check*31 + lists[l][i] + add) % 1000000007
		}
	}
	fmt.Printf("100 answers: %d consecutive, checksum %d\n", yes, check)
}
