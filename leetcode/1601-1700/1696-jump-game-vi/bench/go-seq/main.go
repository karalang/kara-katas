// LeetCode #1696: Jump Game VI -- the bench's Go mirror: the ★ arm on 50
// random arrays of 100000 values from -10^4 to 10^4, each with a random k
// up to 100000, all drawn first, each answered 20 times. Go has no deque;
// the indexes only go on at the back, so a slice with a head and a tail
// holds them.
package main

import "fmt"

func maxResult(nums []int32, k int64) int32 {
	n := int64(len(nums))
	best := make([]int32, n)
	reach := make([]int64, n)
	head, tail := 0, 0
	best[0] = nums[0]
	reach[tail] = 0
	tail++
	for i := int64(1); i < n; i++ {
		if reach[head] < i-k {
			head++
		}
		best[i] = nums[i] + best[reach[head]]
		for tail > head && best[reach[tail-1]] <= best[i] {
			tail--
		}
		reach[tail] = i
		tail++
	}
	return best[n-1]
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1696

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds, n = 50, 20, 100000
	arrays := make([][]int32, count)
	ks := make([]int64, count)
	for c := range arrays {
		arrays[c] = make([]int32, n)
		for i := range arrays[c] {
			arrays[c][i] = int32(nextRandom()%20001 - 10000)
		}
		hi := nextRandom()
		ks[c] = (hi*32768+nextRandom())%n + 1
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for c, nums := range arrays {
			answer := int64(maxResult(nums, ks[c]))
			total += answer
			check = ((check*31+answer+r)%1000000007 + 1000000007) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d values, %d rounds: answers sum to %d, checksum %d\n", count, n, rounds, total, check)
}
