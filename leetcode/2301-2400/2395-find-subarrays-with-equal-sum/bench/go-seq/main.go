// LeetCode #2395: Find Subarrays With Equal Sum -- the bench, the ★ arm in
// Go: each neighbouring pair's sum into a map used as a set, a sum
// already there the answer.
package main

import "fmt"

var seed int64 = 2395

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func findSubarrays(nums []int64) bool {
	seen := map[int64]struct{}{}
	for i := 1; i < len(nums); i++ {
		sum := nums[i-1] + nums[i]
		if _, ok := seen[sum]; ok {
			return true
		}
		seen[sum] = struct{}{}
	}
	return false
}

func main() {
	arrays := make([][]int64, 100)
	for a := range arrays {
		top := 1000 + wide()%1000000
		arr := make([]int64, 1000)
		for i := range arr {
			arr[i] = wide()%(2*top+1) - top
		}
		arrays[a] = arr
	}
	var check, yes int64
	for p := int64(0); p < 2000; p++ {
		for _, a := range arrays {
			found := findSubarrays(a)
			v := int64(1)
			if found {
				v = 2
				yes++
			}
			check = (check*31 + v + p) % 1000000007
		}
	}
	fmt.Printf("2000 passes over 100 arrays of 1000 values: checksum %d, %d yes\n", check, yes)
}
