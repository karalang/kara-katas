// LeetCode #2113: Elements in Array After Removing and Replacing Elements
// -- the benchmark, the same algorithm as elements.kara: each query's
// minute modulo the period `2n`, then one value or -1 for its phase.

package main

import "fmt"

type query struct{ time, index int64 }

func elementInNums(nums []int64, queries []query) []int64 {
	n := int64(len(nums))
	ans := []int64{}
	for _, q := range queries {
		t := q.time % (2 * n)
		if t < n {
			if q.index < n-t {
				ans = append(ans, nums[t+q.index])
			} else {
				ans = append(ans, -1)
			}
		} else if q.index < t-n {
			ans = append(ans, nums[q.index])
		} else {
			ans = append(ans, -1)
		}
	}
	return ans
}

var seed int64 = 2113

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int64, 20)
	for a := range arrays {
		nums := make([]int64, 100)
		for i := range nums {
			nums[i] = nextRandom() % 101
		}
		arrays[a] = nums
	}
	queries := make([]query, 100000)
	for j := range queries {
		time := nextRandom() % 100001
		queries[j] = query{time, nextRandom() % 100}
	}
	var total, check int64
	for s := 0; s < 50; s++ {
		j := s * 1999 % 100000
		queries[j].time++
		var sum int64
		for _, x := range elementInNums(arrays[s%20], queries) {
			sum += x
		}
		total += sum
		check = (check*31 + sum) % 1000000007
	}
	fmt.Printf("50 solves: %d summed, checksum %d\n", total, check)
}
