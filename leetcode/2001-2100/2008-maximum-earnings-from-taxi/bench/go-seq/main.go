// LeetCode #2008: Maximum Earnings From Taxi -- the ★ arm's benchmark, a
// mirror of taxi.kara.
package main

import "fmt"

type ride struct{ start, end, tip int64 }
type leg struct{ start, earned int64 }

func maxTaxiEarnings(n int64, rides []ride) int64 {
	ending := make([][]leg, n+1)
	for _, r := range rides {
		ending[r.end] = append(ending[r.end], leg{r.start, r.end - r.start + r.tip})
	}
	best := make([]int64, n+1)
	for p := int64(2); p <= n; p++ {
		best[p] = best[p-1]
		for _, l := range ending[p] {
			if c := best[l.start] + l.earned; c > best[p] {
				best[p] = c
			}
		}
	}
	return best[n]
}

var seed int64 = 2008

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	roads := make([][]ride, 0, 80)
	for a := 0; a < 80; a++ {
		rides := make([]ride, 0, 5000)
		for i := 0; i < 5000; i++ {
			length := nextRandom()%100 + 1
			start := nextRandom()%(9900-length) + 1
			rides = append(rides, ride{start, start + length, nextRandom() % 1001})
		}
		roads = append(roads, rides)
	}
	var calls, sum, check int64
	for r := int64(0); r < 25; r++ {
		for _, road := range roads {
			answer := maxTaxiEarnings(10000-r*4, road)
			calls++
			sum += answer
			check = (check*31 + answer) % 1000000007
		}
	}
	fmt.Printf("%d calls: sum %d, checksum %d\n", calls, sum, check)
}
