// LeetCode #1673: Find the Most Competitive Subsequence -- the bench's Go
// mirror: the ★ arm on 50 arrays of 100000 values up to 10^9, each with a
// random k, all drawn first, each answered 20 times.
package main

import "fmt"

func mostCompetitive(nums []int32, k int32) []int32 {
	n := int64(len(nums))
	kk := int64(k)
	var stack []int32
	for i := int64(0); i < n; i++ {
		for len(stack) > 0 && stack[len(stack)-1] > nums[i] && int64(len(stack))-1+n-i >= kk {
			stack = stack[:len(stack)-1]
		}
		if int64(len(stack)) < kk {
			stack = append(stack, nums[i])
		}
	}
	return stack
}

var seed int64 = 1673

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const arrays = 50
	const n = 100000
	const rounds = 20
	type problem struct {
		nums []int32
		k    int32
	}
	cases := make([]problem, 0, arrays)
	for a := 0; a < arrays; a++ {
		nums := make([]int32, n)
		for i := range nums {
			nums[i] = int32((nextRandom()*32768 + nextRandom()) % 1000000000)
		}
		k := int32((nextRandom()*32768+nextRandom())%n + 1)
		cases = append(cases, problem{nums, k})
	}
	var chosen, check int64
	for r := int64(0); r < rounds; r++ {
		for _, c := range cases {
			answer := mostCompetitive(c.nums, c.k)
			chosen += int64(len(answer))
			check = (check*31 + int64(answer[0]) + int64(answer[len(answer)-1]) + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d values, %d rounds: %d chosen, checksum %d\n", arrays, n, rounds, chosen, check)
}
