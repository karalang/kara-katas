// LeetCode #2187: Minimum Time to Complete Trips -- the benchmark's Go
// mirror of trips.kara, over a slice of the row: a binary search over
// the time with the count cut at the total.
package main

import "fmt"

func tripsBy(time []int64, t, totalTrips int64) int64 {
	var trips int64
	for _, x := range time {
		trips += t / x
		if trips >= totalTrips {
			break
		}
	}
	return trips
}

func minimumTime(time []int64, totalTrips int64) int64 {
	fastest := time[0]
	for _, x := range time {
		if x < fastest {
			fastest = x
		}
	}
	var lo int64 = 1
	hi := fastest * totalTrips
	for lo < hi {
		mid := lo + (hi-lo)/2
		if tripsBy(time, mid, totalTrips) >= totalTrips {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return lo
}

var seed int64 = 2187

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func bigRandom() int64 {
	a := nextRandom()
	b := nextRandom()
	return a*32768 + b
}

func main() {
	row := make([]int64, 1000000)
	for i := range row {
		row[i] = bigRandom()%10000000 + 1
	}
	var check int64
	for r := 0; r < 200; r++ {
		start := bigRandom() % 900001
		trips := bigRandom()%10000000 + 1
		t := minimumTime(row[start:start+100000], trips)
		check = (check*31 + t%1000000007) % 1000000007
	}
	fmt.Printf("200 solves: checksum %d\n", check)
}
