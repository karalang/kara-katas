// LeetCode #930: Binary Subarrays With Sum -- bench: prefix sums counted
// in an array. Mirrors num_subarrays_with_sum.kara.
package main

import "fmt"

func numSubarraysWithSum(nums []int64, goal int64) int64 {
	seen := make([]int64, len(nums)+1)
	seen[0] = 1
	var sum, count int64
	for _, v := range nums {
		sum += v
		if sum >= goal {
			count += seen[sum-goal]
		}
		seen[sum]++
	}
	return count
}

var seed int64 = 930

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const rounds, count, n = 100, 100, 30000
	// count arrays of n elements, built once, each leaning from 0 to 1 by
	// a random amount, with a goal from 0 to the number of 1s
	arrays := make([][]int64, count)
	goals := make([]int64, count)
	for g := range arrays {
		lean := 1 + nextRandom()%99
		nums := make([]int64, n)
		var ones int64
		for i := range nums {
			if nextRandom()%100 < lean {
				nums[i] = 1
				ones++
			}
		}
		goals[g] = nextRandom() % (ones + 1)
		arrays[g] = nums
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		// each round visits every array, starting from a different one
		for i := 0; i < count; i++ {
			p := (r + i) % count
			a := numSubarraysWithSum(arrays[p], goals[p])
			total += a
			check = (check*1000003 + a) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d arrays of %d: answers summing to %d, checksum %d\n", rounds, count, n, total, check)
}
