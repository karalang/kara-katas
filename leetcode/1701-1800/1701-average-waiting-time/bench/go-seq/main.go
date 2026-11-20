// LeetCode #1701: Average Waiting Time -- the bench's Go mirror: the ★ arm
// on 50 random lists of 100000 customers, arrivals and times up to 10^4,
// all drawn first, each answered 60 times.
package main

import (
	"fmt"
	"math"
)

func averageWaitingTime(customers [][2]int32) float64 {
	var finish, waited int64
	for _, c := range customers {
		finish = max(finish, int64(c[0])) + int64(c[1])
		waited += finish - int64(c[0])
	}
	return float64(waited) / float64(len(customers))
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1701

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds, n = 50, 60, 100000
	lists := make([][][2]int32, count)
	for c := range lists {
		lists[c] = make([][2]int32, n)
		var arrival int64
		for i := range lists[c] {
			if nextRandom()%10 == 0 && arrival < 9999 {
				arrival++
			}
			lists[c][i] = [2]int32{int32(arrival + 1), int32(nextRandom()%10000 + 1)}
		}
	}
	total := 0.0
	var check int64
	for r := int64(0); r < rounds; r++ {
		for _, customers := range lists {
			answer := averageWaitingTime(customers)
			total += answer
			check = (check*31 + int64(math.Round(answer*100000.0)) + r) % 1000000007
		}
	}
	fmt.Printf("%d lists of %d customers, %d rounds: answers sum to %.5f, checksum %d\n", count, n, rounds, total, check)
}
