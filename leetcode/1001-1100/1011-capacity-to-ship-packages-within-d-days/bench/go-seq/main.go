// LeetCode #1011 bench: the ★ arm (binary search on the capacity) over 20
// rows of 50,000 packages, drawn once; each of 20 rounds ships every row,
// each call with its own number of days, and folds each capacity into a
// checksum.
package main

import "fmt"

func shipWithinDays(weights []int64, days int64) int64 {
	var lo, hi int64
	for _, w := range weights {
		if w > lo {
			lo = w
		}
		hi += w
	}
	for lo < hi {
		mid := lo + (hi-lo)/2
		if daysNeeded(weights, mid) <= days {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return lo
}

func daysNeeded(weights []int64, capacity int64) int64 {
	var used, load int64 = 1, 0
	for _, w := range weights {
		if load+w > capacity {
			used++
			load = 0
		}
		load += w
	}
	return used
}

var seed int64 = 1011

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count, rounds := 20, 20
	rows := make([][]int64, count)
	for k := range rows {
		rows[k] = make([]int64, 50000)
		for i := range rows[k] {
			rows[k][i] = 1 + nextRandom()%500
		}
	}
	var check int64
	for r := 0; r < rounds; r++ {
		for k := 0; k < count; k++ {
			days := 1 + (int64(r*count+k)*7919)%50000
			check = (check*31 + shipWithinDays(rows[k], days)) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d rows of 50000 packages: checksum %d\n", rounds, count, check)
}
