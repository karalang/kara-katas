// LeetCode #1244 bench, in Go: the ★ arm (each player's total in a map; a
// top sorts the totals from the highest and adds the first k) on 100
// sessions of 3000 random calls on players up to 10000; the tops' answers
// folded into a checksum.
package main

import (
	"fmt"
	"sort"
)

type Leaderboard struct {
	scores map[int64]int64
}

func NewLeaderboard() *Leaderboard {
	return &Leaderboard{scores: map[int64]int64{}}
}

func (b *Leaderboard) AddScore(player, score int64) {
	b.scores[player] += score
}

func (b *Leaderboard) Top(k int64) int64 {
	all := make([]int64, 0, len(b.scores))
	for _, v := range b.scores {
		all = append(all, v)
	}
	sort.Slice(all, func(i, j int) bool { return all[i] > all[j] })
	var sum int64
	for i := int64(0); i < k; i++ {
		sum += all[i]
	}
	return sum
}

func (b *Leaderboard) Reset(player int64) {
	delete(b.scores, player)
}

var seed int64 = 1244

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func session(calls, players int64) (int64, int64) {
	board := NewLeaderboard()
	on := []int64{}
	var check, tops int64
	for c := int64(0); c < calls; c++ {
		op := nextRandom() % 4
		if op <= 1 || len(on) == 0 {
			player := nextRandom()%players + 1
			score := nextRandom()%100 + 1
			board.AddScore(player, score)
			seen := false
			for _, p := range on {
				if p == player {
					seen = true
					break
				}
			}
			if !seen {
				on = append(on, player)
			}
		} else if op == 2 {
			got := board.Top(nextRandom()%int64(len(on)) + 1)
			check = (check*131 + got) % 1000000007
			tops++
		} else {
			i := nextRandom() % int64(len(on))
			player := on[i]
			on[i] = on[len(on)-1]
			on = on[:len(on)-1]
			board.Reset(player)
		}
	}
	return tops, check
}

func main() {
	var tops, check int64
	for s := 0; s < 100; s++ {
		t, c := session(3000, 10000)
		tops += t
		check = (check*31 + c) % 1000000007
	}
	fmt.Printf("100 sessions of 3000 calls on 10000 players: %d tops, checksum %d\n", tops, check)
}
