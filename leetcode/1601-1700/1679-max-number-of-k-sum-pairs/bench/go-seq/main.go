// LeetCode #1679: Max Number of K-Sum Pairs -- the bench's Go mirror: the ★
// arm on 50 arrays of 100000 values up to 100000, each with a k up to
// 200000, all drawn first, each answered 10 times, with a map.

package main

import "fmt"

func maxOperations(nums []int32, k int32) int32 {
	waiting := make(map[int32]int32)
	var operations int32
	for _, x := range nums {
		partner := k - x
		if c, ok := waiting[partner]; ok && c > 0 {
			waiting[partner] = c - 1
			operations++
		} else {
			waiting[x]++
		}
	}
	return operations
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1679

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const arrays = 50
	const n = 100000
	const most = 100000
	const rounds = 10
	type problem struct {
		nums []int32
		k    int32
	}
	cases := make([]problem, 0, arrays)
	for a := 0; a < arrays; a++ {
		nums := make([]int32, n)
		for i := range nums {
			nums[i] = int32((nextRandom()*32768+nextRandom())%most + 1)
		}
		k := int32((nextRandom()*32768+nextRandom())%(2*most-1) + 2)
		cases = append(cases, problem{nums, k})
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, c := range cases {
			operations := int64(maxOperations(c.nums, c.k))
			total += operations
			check = (check*31 + operations + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d values, %d rounds: %d operations, checksum %d\n", arrays, n, rounds, total, check)
}
