// LeetCode #2398: Maximum Number of Robots Within Budget -- the bench, the
// ★ arm in Go: a sliding window, its largest charge time kept by a
// monotonic deque in a slice.
package main

import "fmt"

var seed int64 = 2398

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func maximumRobots(charge, running []int64, budget int64) int64 {
	largest := []int{}
	var best, sum int64
	left := 0
	for right := range charge {
		sum += running[right]
		for len(largest) > 0 && charge[largest[len(largest)-1]] <= charge[right] {
			largest = largest[:len(largest)-1]
		}
		largest = append(largest, right)
		for left <= right && charge[largest[0]]+int64(right-left+1)*sum > budget {
			if largest[0] == left {
				largest = largest[1:]
			}
			sum -= running[left]
			left++
		}
		if int64(right-left+1) > best {
			best = int64(right - left + 1)
		}
	}
	return best
}

func main() {
	type fleet struct{ charge, running []int64 }
	fleets := make([]fleet, 20)
	for f := range fleets {
		charge := make([]int64, 50000)
		for i := range charge {
			charge[i] = 1 + wide()%100000
		}
		running := make([]int64, 50000)
		for i := range running {
			running[i] = 1 + wide()%100000
		}
		fleets[f] = fleet{charge, running}
	}
	var check int64
	for p := int64(0); p < 2; p++ {
		for _, fl := range fleets {
			for budget := int64(100000); budget <= 1000000000000000; budget *= 10 {
				check = (check*31 + maximumRobots(fl.charge, fl.running, budget) + p) % 1000000007
			}
		}
	}
	fmt.Printf("2 passes over 20 fleets of 5 * 10^4 robots, 11 budgets: checksum %d\n", check)
}
