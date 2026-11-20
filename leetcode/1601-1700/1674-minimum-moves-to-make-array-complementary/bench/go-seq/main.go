// LeetCode #1674: Minimum Moves to Make Array Complementary -- the bench's Go
// mirror: the ★ arm on 100 arrays of 100000 values with limits up to
// 100000, all drawn first, each answered 20 times.
package main

import "fmt"

func minMoves(nums []int32, limit int32) int32 {
	n := len(nums)
	lim := int64(limit)
	delta := make([]int64, 2*lim+2)
	for i := 0; i < n/2; i++ {
		a := int64(min(nums[i], nums[n-1-i]))
		b := int64(max(nums[i], nums[n-1-i]))
		delta[2] += 2
		delta[a+1] -= 1
		delta[a+b] -= 1
		delta[a+b+1] += 1
		delta[b+lim+1] += 1
	}
	best := int64(n)
	var moves int64
	for sum := int64(2); sum <= 2*lim; sum++ {
		moves += delta[sum]
		best = min(best, moves)
	}
	return int32(best)
}

var seed int64 = 1674

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const arrays = 100
	const n = 100000
	const rounds = 20
	type problem struct {
		nums  []int32
		limit int32
	}
	cases := make([]problem, 0, arrays)
	for a := 0; a < arrays; a++ {
		limit := (nextRandom()*32768+nextRandom())%100000 + 1
		nums := make([]int32, n)
		for i := range nums {
			nums[i] = int32((nextRandom()*32768+nextRandom())%limit + 1)
		}
		cases = append(cases, problem{nums, int32(limit)})
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, c := range cases {
			moves := int64(minMoves(c.nums, c.limit))
			total += moves
			check = (check*31 + moves + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d values, %d rounds: %d moves, checksum %d\n", arrays, n, rounds, total, check)
}
