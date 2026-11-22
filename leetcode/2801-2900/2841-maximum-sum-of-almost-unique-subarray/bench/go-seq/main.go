// LeetCode #2841: Maximum Sum of Almost Unique Subarray -- the bench,
// mirrored from almost.kara: a window of k slid along the array, its
// sum kept and a map from each value in it to its count.
package main

import "fmt"

func maxSum(nums []int64, m, k int64) int64 {
	count := map[int64]int64{}
	var sum, best int64
	for i := int64(0); i < int64(len(nums)); i++ {
		count[nums[i]]++
		sum += nums[i]
		if i >= k {
			out := nums[i-k]
			sum -= out
			left := count[out] - 1
			if left == 0 {
				delete(count, out)
			} else {
				count[out] = left
			}
		}
		if i+1 >= k && int64(len(count)) >= m && sum > best {
			best = sum
		}
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, n, rounds = 100, 20000, 20
	seed := int64(2841)
	type caseT struct {
		nums []int64
		m, k int64
	}
	cases := make([]caseT, 0, count)
	for c := 0; c < count; c++ {
		nums := make([]int64, n)
		for i := range nums {
			nums[i] = nextRandom(&seed)%10000 + 1
		}
		k := nextRandom(&seed)%5000 + 1
		m := nextRandom(&seed)%k + 1
		cases = append(cases, caseT{nums, m, k})
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, cs := range cases {
			best := maxSum(cs.nums, cs.m, cs.k)
			total += best
			check = (check*31 + best + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d, %d rounds: sums total %d, checksum %d\n", count, n, rounds, total, check)
}
