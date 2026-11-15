// LeetCode #1578 bench: the same one pass, in Go.
package main

import "fmt"

var seed int64 = 1578

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func minCost(colors string, neededTime []int64) int64 {
	var total, keep int64
	for i := 0; i < len(colors); i++ {
		if i > 0 && colors[i] != colors[i-1] {
			keep = 0
		}
		total += min(keep, neededTime[i])
		keep = max(keep, neededTime[i])
	}
	return total
}

type rope struct {
	colors string
	times  []int64
}

func main() {
	ropes := make([]rope, 0, 200)
	for r := 0; r < 200; r++ {
		colors := make([]byte, 0)
		times := make([]int64, 0)
		for i := 0; i < 100000; i++ {
			colors = append(colors, byte('a'+nextRandom()%3))
			times = append(times, nextRandom()%1000+1)
		}
		ropes = append(ropes, rope{string(colors), times})
	}
	var check, total int64
	for _, r := range ropes {
		cost := minCost(r.colors, r.times)
		total += cost
		check = mix(check, cost)
	}
	fmt.Printf("200 ropes of 100000 balloons: time total %d, checksum %d\n", total, check)
}
