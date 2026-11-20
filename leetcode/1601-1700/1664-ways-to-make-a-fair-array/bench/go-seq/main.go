// LeetCode #1664 bench: the ★ arm, one pass with running sums.
//
// 20 arrays of 10^5 values from 1 to 2, LeetCode's largest length, drawn
// first; then each is answered 50 times.
package main

import "fmt"

func waysToMakeFair(nums []int32) int32 {
	var total [2]int32
	for i, x := range nums {
		total[i%2] += x
	}
	var before [2]int32
	var ways int32
	for i, x := range nums {
		p := i % 2
		after := [2]int32{total[0] - before[0], total[1] - before[1]}
		after[p] -= x
		if before[0]+after[1] == before[1]+after[0] {
			ways++
		}
		before[p] += x
	}
	return ways
}

var seed int64

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, n, rounds = 20, 100000, 50
	seed = 1664
	arrays := make([][]int32, count)
	for c := range arrays {
		nums := make([]int32, n)
		for i := range nums {
			nums[i] = int32(nextRandom()%2 + 1)
		}
		arrays[c] = nums
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range arrays {
			answer := int64(waysToMakeFair(nums))
			total += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d values, %d rounds: %d fair removals, checksum %d\n", count, n, rounds, total, check)
}
