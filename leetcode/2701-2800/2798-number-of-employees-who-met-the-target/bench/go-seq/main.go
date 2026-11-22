// LeetCode #2798: Number of Employees Who Met the Target -- the bench in
// Go: the ★ arm over 20000 teams of 50 with hours and targets up to
// 10^5, all drawn first, then each answered 500 times.
package main

import "fmt"

func numberOfEmployeesWhoMetTarget(hours []int64, target int64) int64 {
	var met int64
	for _, h := range hours {
		if h >= target {
			met++
		}
	}
	return met
}

var seed int64 = 2798

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	count := 20000
	rounds := 500
	hours := make([][]int64, count)
	targets := make([]int64, count)
	for c := 0; c < count; c++ {
		hours[c] = make([]int64, 50)
		for i := range hours[c] {
			hours[c][i] = wide() % 100001
		}
		targets[c] = wide() % 100001
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for c := 0; c < count; c++ {
			a := numberOfEmployeesWhoMetTarget(hours[c], targets[c])
			total += a
			check = (check*31 + a + r) % 1000000007
		}
	}
	fmt.Printf("%d teams of 50, %d rounds: met sum to %d, checksum %d\n", count, rounds, total, check)
}
