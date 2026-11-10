// LeetCode #2059: Minimum Operations to Convert Number -- Go mirror of the
// ★ arm's benchmark (../ops.kara): the same 16000 problems, each answered
// by one breadth-first search over the values 0 to 1000, the queue a
// slice read from a moving head.
package main

import "fmt"

type state struct{ x, steps int64 }

func minimumOperations(nums []int64, start, goal int64) int64 {
	seen := make([]bool, 1001)
	queue := []state{{start, 0}}
	seen[start] = true
	for head := 0; head < len(queue); head++ {
		s := queue[head]
		for _, n := range nums {
			for _, y := range [3]int64{s.x + n, s.x - n, s.x ^ n} {
				if y == goal {
					return s.steps + 1
				}
				if y >= 0 && y <= 1000 && !seen[y] {
					seen[y] = true
					queue = append(queue, state{y, s.steps + 1})
				}
			}
		}
	}
	return -1
}

var seed int64 = 2059

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func draw(n, spread int64) []int64 {
	nums := []int64{}
	for int64(len(nums)) < n {
		var x int64
		if nextRandom()%8 == 0 {
			hi := nextRandom()
			x = (hi*32768+nextRandom())%2000000001 - 1000000000
		} else {
			x = nextRandom()%(2*spread+1) - spread
		}
		dup := false
		for _, v := range nums {
			if v == x {
				dup = true
				break
			}
		}
		if !dup {
			nums = append(nums, x)
		}
	}
	return nums
}

func main() {
	spreads := [4]int64{5, 50, 300, 1500}
	var unreachable, total, check int64
	for r := 0; r < 16000; r++ {
		n := nextRandom()%16 + 1
		spread := spreads[nextRandom()%4]
		nums := draw(n, spread)
		start := nextRandom() % 1001
		goal := nextRandom()%1401 - 200
		if goal == start {
			goal++
		}
		ops := minimumOperations(nums, start, goal)
		if ops < 0 {
			unreachable++
		}
		total += ops
		check = (check*31 + ops + 2) % 1000000007
	}
	fmt.Printf("16000 problems: %d unreachable, sum %d, checksum %d\n", unreachable, total, check)
}
