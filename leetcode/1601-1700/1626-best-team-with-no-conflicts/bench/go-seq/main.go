// LeetCode #1626: Best Team With No Conflicts -- the bench in Go,
// mirroring team.kara: sorted by (age, score), the best team ending at
// each player from every earlier player scoring no higher.
package main

import (
	"fmt"
	"sort"
)

type player struct{ age, score int32 }

func bestTeamScore(scores, ages []int32) int32 {
	n := len(scores)
	players := make([]player, n)
	for i := range players {
		players[i] = player{ages[i], scores[i]}
	}
	sort.Slice(players, func(a, b int) bool {
		if players[a].age != players[b].age {
			return players[a].age < players[b].age
		}
		return players[a].score < players[b].score
	})
	best := make([]int64, n)
	var answer int64
	for i := 0; i < n; i++ {
		score := int64(players[i].score)
		best[i] = score
		for j := 0; j < i; j++ {
			if int64(players[j].score) <= score && best[j]+score > best[i] {
				best[i] = best[j] + score
			}
		}
		if best[i] > answer {
			answer = best[i]
		}
	}
	return int32(answer)
}

var seed int64 = 1626

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	type team struct{ scores, ages []int32 }
	teams := make([]team, 0, 100)
	for t := 0; t < 100; t++ {
		scores := make([]int32, 1000)
		ages := make([]int32, 1000)
		for i := 0; i < 1000; i++ {
			high := nextRandom()
			scores[i] = int32((high*32768+nextRandom())%1000000 + 1)
			ages[i] = int32(nextRandom()%1000 + 1)
		}
		teams = append(teams, team{scores, ages})
	}
	var check, total int64
	for _, t := range teams {
		got := int64(bestTeamScore(t.scores, t.ages))
		total += got
		check = (check*31 + got + 1) % 1000000007
	}
	fmt.Printf("100 teams of 1000 players: best scores sum to %d, checksum %d\n", total, check)
}
