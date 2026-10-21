// Benchmark for #825: Friends Of Appropriate Ages -- the ★ arm (counts by age).
//
// Mirrors num_friend_requests.kara: the people counted by age once, and
// every pair of ages tested with the statement's three conditions, each
// pair that passes adding one request from every person of the first age
// to every person of the second, but for a person and themself.
package main

import "fmt"

func asks(x, y int64) bool {
	return !(2*y <= x+14 || y > x || (y > 100 && x < 100))
}

func numFriendRequests(ages []int64) int64 {
	count := make([]int64, 121)
	for _, a := range ages {
		count[a]++
	}
	var requests int64
	for x := int64(1); x < 121; x++ {
		if count[x] == 0 {
			continue
		}
		for y := int64(1); y < 121; y++ {
			if count[y] > 0 && asks(x, y) {
				requests += count[x] * count[y]
				if x == y {
					requests -= count[x]
				}
			}
		}
	}
	return requests
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := 64
	rounds := 50000
	seed := int64(825)
	lists := make([][]int64, 0, count)
	for g := 0; g < count; g++ {
		ages := make([]int64, 0, 20000)
		for i := 0; i < 20000; i++ {
			ages = append(ages, 1+nextRandom(&seed)%120)
		}
		lists = append(lists, ages)
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		r := numFriendRequests(lists[round%count])
		total += r
		checksum = (checksum*131 + r) % 1000000007
	}
	fmt.Printf("%d rounds of %d lists: total %d, checksum %d\n", rounds, count, total, checksum)
}
