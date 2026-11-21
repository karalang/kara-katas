// LeetCode #2420: Find All Good Indices -- the bench, the ★ arm: the run of
// values ending at each index without rising, from the left, and the run
// starting at each index without falling, from the right.
package main

import "fmt"

var seed int64 = 2420

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func goodIndices(nums []int64, k int) []int {
	n := len(nums)
	falling := make([]int, n)
	rising := make([]int, n)
	falling[0] = 1
	for i := 1; i < n; i++ {
		falling[i] = 1
		if nums[i] <= nums[i-1] {
			falling[i] = falling[i-1] + 1
		}
	}
	rising[n-1] = 1
	for i := n - 2; i >= 0; i-- {
		rising[i] = 1
		if nums[i] <= nums[i+1] {
			rising[i] = rising[i+1] + 1
		}
	}
	good := []int{}
	for i := k; i < n-k; i++ {
		if falling[i-1] >= k && rising[i+1] >= k {
			good = append(good, i)
		}
	}
	return good
}

func main() {
	arrays := make([][]int64, 10)
	for a := range arrays {
		nums := make([]int64, 0, 100000)
		down := true
		for i := 0; i < 100000; i++ {
			if i == 0 {
				hi := nextRandom()
				nums = append(nums, 1+(hi*32768+nextRandom())%1000000)
			} else {
				if nextRandom()%60 == 0 {
					down = !down
				}
				d := nextRandom() % 41
				v := nums[i-1] + d
				if down {
					v = nums[i-1] - d
				}
				nums = append(nums, min(max(v, 1), 1000000))
			}
		}
		arrays[a] = nums
	}
	check := int64(0)
	for p := 0; p < 100; p++ {
		for a := 0; a < 10; a++ {
			good := goodIndices(arrays[a], 1+(p+a)%40)
			sum := 0
			for _, g := range good {
				sum += g
			}
			check = (check*31 + int64(len(good)) + int64(sum%1000003)) % 1000000007
		}
	}
	fmt.Printf("100 passes over 10 arrays of 10^5 values: checksum %d\n", check)
}
