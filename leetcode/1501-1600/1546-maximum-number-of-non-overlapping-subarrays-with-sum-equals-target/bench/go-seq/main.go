// LeetCode #1546: Maximum Number of Non-Overlapping Subarrays With Sum Equals
// Target -- bench: the ★ arm (greedy, a set of prefix sums cleared at each
// cut) over 100 arrays of 1 to 100000 values in -10..10, each with a target
// in -20..20, built once, each asked 5 times. Go mirror of subarrays.kara,
// with a map as the set and clear() to clear it.
package main

import "fmt"

func maxNonOverlapping(nums []int64, target int64) int64 {
	seen := map[int64]struct{}{0: {}}
	sum, count := int64(0), int64(0)
	for _, x := range nums {
		sum += x
		if _, ok := seen[sum-target]; ok {
			count++
			clear(seen)
			seen[0] = struct{}{}
			sum = 0
		} else {
			seen[sum] = struct{}{}
		}
	}
	return count
}

var seed int64 = 1546

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	type cs struct {
		nums   []int64
		target int64
	}
	cases := make([]cs, 0, 100)
	for k := 0; k < 100; k++ {
		a := nextRandom()
		n := (a*32768+nextRandom())%100000 + 1
		nums := make([]int64, n)
		for i := range nums {
			nums[i] = nextRandom()%21 - 10
		}
		target := nextRandom()%41 - 20
		cases = append(cases, cs{nums, target})
	}
	check, total := int64(0), int64(0)
	for p := 0; p < 5; p++ {
		for _, c := range cases {
			answer := maxNonOverlapping(c.nums, c.target)
			total += answer
			check = mix(check, answer)
		}
	}
	fmt.Printf("5 passes over 100 arrays of up to 100000 values: %d subarrays, checksum %d\n", total, check)
}
