// LeetCode #2412: Minimum Money Required Before Transactions -- the bench,
// the ★ arm in Go: the total loss, and the largest of the losing
// transactions' cashbacks and the gaining ones' costs.

package main

import "fmt"

var seed int64 = 2412

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func minimumMoney(transactions [][2]int64) int64 {
	var loss, extra int64
	for _, t := range transactions {
		cost, cashback := t[0], t[1]
		if cost > cashback {
			loss += cost - cashback
			extra = max(extra, cashback)
		} else {
			extra = max(extra, cost)
		}
	}
	return loss + extra
}

func main() {
	lists := make([][][2]int64, 10)
	top := int64(1)
	for i := range lists {
		top *= 7
		ts := make([][2]int64, 100000)
		for j := range ts {
			cost := (nextRandom()*32768 + nextRandom()) % (top + 1)
			ts[j] = [2]int64{cost, (nextRandom()*32768 + nextRandom()) % (top + 1)}
		}
		lists[i] = ts
	}
	var check int64
	for p := int64(0); p < 100; p++ {
		for _, ts := range lists {
			check = (check*31 + minimumMoney(ts) + p) % 1000000007
		}
	}
	fmt.Printf("100 passes over 10 lists of 10^5 transactions: checksum %d\n", check)
}
