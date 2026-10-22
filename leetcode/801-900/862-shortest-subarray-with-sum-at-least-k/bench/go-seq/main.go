// LeetCode #862: Shortest Subarray with Sum at Least K -- Go mirror of the
// bench program (the ★ arm, prefix sums and a deque of candidate starts;
// the deque is a slice with a head and a tail, since every index enters
// it once).
package main

import "fmt"

func shortestSubarray(nums []int64, k int64) int64 {
	n := len(nums)
	p := make([]int64, 1, n+1)
	for _, x := range nums {
		p = append(p, p[len(p)-1]+x)
	}
	best := n + 1
	starts := make([]int, n+1)
	head, tail := 0, 0
	for j := 0; j < n+1; j++ {
		for head < tail && p[j]-p[starts[head]] >= k {
			if j-starts[head] < best {
				best = j - starts[head]
			}
			head++
		}
		for head < tail && p[starts[tail-1]] >= p[j] {
			tail--
		}
		starts[tail] = j
		tail++
	}
	if best <= n {
		return int64(best)
	}
	return -1
}

var seed int64 = 862

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomValue() int64 {
	hi := nextRandom()
	lo := nextRandom()
	return (hi*32768+lo)%200001 - 100000
}

func main() {
	var n int64 = 100000
	var k int64 = 5000000
	rounds := 300
	nums := make([]int64, n)
	for i := range nums {
		nums[i] = randomValue()
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		hi := nextRandom()
		lo := nextRandom()
		i := (hi*32768 + lo) % n
		old := nums[i]
		nums[i] = randomValue()
		got := shortestSubarray(nums, k)
		nums[i] = old
		total += got
		check = (check*31 + got + 2) % 1000000007
	}
	fmt.Printf("%d rounds on %d values, k = %d: lengths sum to %d, checksum %d\n", rounds, n, k, total, check)
}
