// LeetCode #2763: Sum of Imbalance Numbers of All Subarrays -- the bench
// (imbalance.kara in Go): each index counted for the subarrays in which
// it is the leftmost occurrence of a run's top value, from the last x or
// x + 1 before it and the first x + 1 after it.
package main

import "fmt"

var seed int64 = 2763

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func sumImbalanceNumbers(nums []int64) int64 {
	n := int64(len(nums))
	left := make([]int64, n)
	last := make([]int64, n+2)
	for v := range last {
		last[v] = -1
	}
	for i, x := range nums {
		left[i] = max(last[x], last[x+1])
		last[x] = int64(i)
	}
	first := make([]int64, n+2)
	for v := range first {
		first[v] = n
	}
	var total int64
	for i := n - 1; i >= 0; i-- {
		x := nums[i]
		total += (i - left[i]) * (first[x+1] - i)
		first[x] = i
	}
	return total - n*(n+1)/2
}

func main() {
	const count, rounds = 20000, 5
	cases := make([][]int64, count)
	for k := range cases {
		a := make([]int64, 1000)
		for i := range a {
			a[i] = nextRandom()%1000 + 1
		}
		cases[k] = a
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range cases {
			found := sumImbalanceNumbers(nums)
			sum += found
			check = (check*31 + found + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of 1000, %d rounds: imbalances sum to %d, checksum %d\n", count, rounds, sum, check)
}
