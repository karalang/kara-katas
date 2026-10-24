// Benchmark: LeetCode #983 Minimum Cost For Tickets -- the ★ arm, a
// table over the calendar, on plans of up to LeetCode's 365 days.
// Mirrors ../mincost_tickets.kara, .rs, .c and .py.
package main

import "fmt"

func mincostTickets(days []int64, costs []int64) int64 {
	last := days[len(days)-1]
	travel := make([]bool, last+1)
	for _, d := range days {
		travel[d] = true
	}
	best := make([]int64, last+1)
	for d := int64(1); d <= last; d++ {
		if !travel[d] {
			best[d] = best[d-1]
			continue
		}
		var week, month int64
		if d >= 7 {
			week = best[d-7]
		}
		if d >= 30 {
			month = best[d-30]
		}
		best[d] = min(best[d-1]+costs[0], week+costs[1], month+costs[2])
	}
	return best[last]
}

var seed int64 = 983

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := 300
	plans := make([][]int64, 1000)
	prices := make([][]int64, 1000)
	for p := range plans {
		n := 1 + nextRandom()%365
		need := n
		var days []int64
		for d := int64(1); d < 366; d++ {
			if need > 0 && nextRandom()%(366-d) < need {
				days = append(days, d)
				need--
			}
		}
		plans[p] = days
		a := 1 + nextRandom()%1000
		b := 1 + nextRandom()%1000
		c := 1 + nextRandom()%1000
		prices[p] = []int64{a, b, c}
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 1000; i++ {
			j := (r + i) % 1000
			c := mincostTickets(plans[j], prices[j])
			total += c
			check = (check*31 + c) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 1000 plans of up to 365 days: cost %d, checksum %d\n", rounds, total, check)
}
