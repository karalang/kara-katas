// Benchmark: LeetCode #1094 Car Pooling -- the ★ arm, a difference array
// over the stops. Mirrors ../car_pooling.kara.
package main

import "fmt"

func carPooling(trips [][]int64, capacity int64) bool {
	change := make([]int64, 1001)
	for _, t := range trips {
		change[t[1]] += t[0]
		change[t[2]] -= t[0]
	}
	var aboard int64
	for _, c := range change {
		aboard += c
		if aboard > capacity {
			return false
		}
	}
	return true
}

var seed int64 = 1094

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][][]int64, 0, 64)
	for j := 0; j < 64; j++ {
		trips := make([][]int64, 0, 1000)
		for i := 0; i < 1000; i++ {
			n := nextRandom()%100 + 1
			a := nextRandom() % 1000
			b := a + 1 + nextRandom()%(1000-a)
			trips = append(trips, []int64{n, a, b})
		}
		lists = append(lists, trips)
	}
	var total, check int64
	for round := int64(0); round < 100; round++ {
		for j := int64(0); j < int64(len(lists)); j++ {
			k := (round*7 + j*13) % 1000
			lists[j][k][0] = 1 + (lists[j][k][0]+round)%100
			var lo, hi int64 = 1, 100000
			for lo < hi {
				mid := (lo + hi) / 2
				if carPooling(lists[j], mid) {
					hi = mid
				} else {
					lo = mid + 1
				}
			}
			total += lo
			check = (check*31 + lo) % 1000000007
		}
	}
	fmt.Printf("100 rounds over 64 lists of 1000 trips: smallest capacities sum to %d, checksum %d\n", total, check)
}
