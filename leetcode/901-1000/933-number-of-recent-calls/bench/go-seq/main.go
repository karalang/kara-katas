// LeetCode #933: Number of Recent Calls -- bench: a queue of the recent
// pings. Mirrors recent_counter.kara, .c, .rs and .py. The queue is a
// slice with its front resliced away, as Go programs commonly write one.

package main

import "fmt"

type RecentCounter struct {
	pings []int64
}

func (c *RecentCounter) ping(t int64) int64 {
	c.pings = append(c.pings, t)
	for c.pings[0] < t-3000 {
		c.pings = c.pings[1:]
	}
	return int64(len(c.pings))
}

var seed int64 = 933

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var rounds int64 = 50
	var count int64 = 100
	var length int64 = 10000
	// count streams of length pings, each from 1 to gap after the one
	// before, gap from 1 to 600 a stream, built once
	streams := make([][]int64, 0, count)
	for s := int64(0); s < count; s++ {
		gap := 1 + nextRandom()%600
		times := make([]int64, 0, length)
		var t int64
		for k := int64(0); k < length; k++ {
			t += 1 + nextRandom()%gap
			times = append(times, t)
		}
		streams = append(streams, times)
	}
	var total int64
	var check int64
	for r := int64(0); r < rounds; r++ {
		// each round plays every stream into a new counter, starting
		// from a different one
		for i := int64(0); i < count; i++ {
			counter := RecentCounter{}
			var last int64
			for _, t := range streams[(r+i)%count] {
				last = counter.ping(t)
				total += last
			}
			check = (check*1000003 + last) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d streams of %d pings: answers summing to %d, checksum %d\n", rounds, count, length, total, check)
}
