// LeetCode #2410: Maximum Matching of Players With Trainers -- the bench,
// the ★ arm in Go: both lists copied and sorted with `slices.Sort`, each
// trainer upward taking the weakest player not yet matched if it is strong
// enough.

package main

import (
	"fmt"
	"slices"
)

var seed int64 = 2410

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func matchPlayersAndTrainers(players, trainers []int64) int64 {
	p := slices.Clone(players)
	t := slices.Clone(trainers)
	slices.Sort(p)
	slices.Sort(t)
	matched := 0
	for _, capacity := range t {
		if matched < len(p) && p[matched] <= capacity {
			matched++
		}
	}
	return int64(matched)
}

func main() {
	type pair struct{ players, trainers []int64 }
	cases := make([]pair, 10)
	for i := range cases {
		players := make([]int64, 100000)
		for j := range players {
			players[j] = 1 + (nextRandom()*32768+nextRandom())%1000000000
		}
		trainers := make([]int64, 100000)
		for j := range trainers {
			trainers[j] = 1 + (nextRandom()*32768+nextRandom())%900000000 + 10000000*int64(i)
		}
		cases[i] = pair{players, trainers}
	}
	var check int64
	for p := int64(0); p < 5; p++ {
		for _, c := range cases {
			check = (check*31 + matchPlayersAndTrainers(c.players, c.trainers) + p) % 1000000007
		}
	}
	fmt.Printf("5 passes over 10 cases of 10^5 players and trainers: checksum %d\n", check)
}
