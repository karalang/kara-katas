// LeetCode #2735: Collecting Chocolates -- the bench (chocolates.kara in
// Go): each type's cheapest price within k turns, narrowed one turn at a
// time, and the least of k x plus their sum.
package main

import "fmt"

func minCost(nums []int64, x int64) int64 {
	n := len(nums)
	cheapest := make([]int64, n)
	copy(cheapest, nums)
	var best int64
	for _, v := range nums {
		best += v
	}
	for k := 1; k < n; k++ {
		for t := 0; t < n; t++ {
			cheapest[t] = min(cheapest[t], nums[(t-k+n)%n])
		}
		var total int64
		for _, v := range cheapest {
			total += v
		}
		best = min(best, int64(k)*x+total)
	}
	return best
}

var seed int64 = 2735

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type problem struct {
	nums []int64
	x    int64
}

func main() {
	const cases, n, rounds = 100, 1000, 3
	problems := []problem{}
	for c := 0; c < cases; c++ {
		nums := make([]int64, n)
		for i := range nums {
			hi := nextRandom()
			nums[i] = (hi*32768+nextRandom())%1000000000 + 1
		}
		hi := nextRandom()
		x := (hi*32768+nextRandom())%10000000 + 1
		problems = append(problems, problem{nums, x})
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, p := range problems {
			cost := minCost(p.nums, p.x)
			sum += cost
			check = (check*31 + cost + r) % 1000000007
		}
	}
	fmt.Printf("%d cases of %d chocolates, %d rounds: costs sum to %d, checksum %d\n", cases, n, rounds, sum, check)
}
