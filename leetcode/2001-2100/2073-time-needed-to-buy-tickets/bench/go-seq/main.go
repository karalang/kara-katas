// LeetCode #2073: Time Needed to Buy Tickets -- Go mirror of the ★ arm's
// benchmark (tickets.kara): 20000 lines of 100 people, every place in
// every line asked about, 2000000 answers.
package main

import "fmt"

func timeRequiredToBuy(tickets []int64, k int) int64 {
	want := tickets[k]
	var time int64
	for i, t := range tickets {
		if i <= k {
			time += min(t, want)
		} else {
			time += min(t, want-1)
		}
	}
	return time
}

var seed int64 = 2073

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lines := make([][]int64, 0, 20000)
	for l := 0; l < 20000; l++ {
		tickets := make([]int64, 0, 100)
		for j := 0; j < 100; j++ {
			tickets = append(tickets, nextRandom()%100+1)
		}
		lines = append(lines, tickets)
	}
	var total, check int64
	for _, tickets := range lines {
		for k := 0; k < 100; k++ {
			a := timeRequiredToBuy(tickets, k)
			total += a
			check = (check*31 + a) % 1000000007
		}
	}
	fmt.Printf("2000000 answers: sum %d, checksum %d\n", total, check)
}
