// LeetCode #1575: Count All Possible Routes -- bench: the ★ arm (routes to
// the finish filled from no fuel up) over 100 problems of 60 distinct
// locations below 300 and a fuel of 200, every problem drawn first.
package main

import "fmt"

func countRoutes(locations []int64, start, finish, fuel int) int64 {
	const m = 1000000007
	n := len(locations)
	ways := make([][]int64, fuel+1)
	for f := range ways {
		ways[f] = make([]int64, n)
	}
	for f := 0; f < fuel+1; f++ {
		for c := 0; c < n; c++ {
			var total int64
			if c == finish {
				total = 1
			}
			for d := 0; d < n; d++ {
				cost := locations[c] - locations[d]
				if cost < 0 {
					cost = -cost
				}
				if d != c && int(cost) <= f {
					total = (total + ways[f-int(cost)][d]) % m
				}
			}
			ways[f][c] = total
		}
	}
	return ways[fuel][start]
}

var seed int64 = 1575

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

type problem struct {
	locations     []int64
	start, finish int
}

func main() {
	const n = 60
	problems := make([]problem, 0, 100)
	for p := 0; p < 100; p++ {
		locations := make([]int64, 0, n)
		for len(locations) < n {
			x := nextRandom() % 300
			seen := false
			for _, y := range locations {
				if y == x {
					seen = true
					break
				}
			}
			if !seen {
				locations = append(locations, x)
			}
		}
		start := int(nextRandom() % n)
		finish := int(nextRandom() % n)
		problems = append(problems, problem{locations, start, finish})
	}
	var check, total int64
	for _, pr := range problems {
		routes := countRoutes(pr.locations, pr.start, pr.finish, 200)
		total += routes
		check = mix(check, routes)
	}
	fmt.Printf("100 problems of %d locations and fuel 200: routes total %d, checksum %d\n", n, total, check)
}
