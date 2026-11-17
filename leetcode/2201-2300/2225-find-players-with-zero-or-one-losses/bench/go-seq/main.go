// LeetCode #2225: Find Players With Zero or One Losses -- the benchmark's
// Go mirror of players.kara: a map of losses, both lists sorted.
package main

import (
	"fmt"
	"sort"
)

func findWinners(matches [][2]int64) [][]int64 {
	losses := map[int64]int64{}
	for _, game := range matches {
		if _, ok := losses[game[0]]; !ok {
			losses[game[0]] = 0
		}
		losses[game[1]]++
	}
	unbeaten := []int64{}
	once := []int64{}
	for player, count := range losses {
		if count == 0 {
			unbeaten = append(unbeaten, player)
		} else if count == 1 {
			once = append(once, player)
		}
	}
	sort.Slice(unbeaten, func(i, j int) bool { return unbeaten[i] < unbeaten[j] })
	sort.Slice(once, func(i, j int) bool { return once[i] < once[j] })
	return [][]int64{unbeaten, once}
}

var seed int64 = 2225

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

// a match between two players of 1 to 10^5, never one against itself
func drawMatch() [2]int64 {
	winner := wideRandom()%100000 + 1
	loser := wideRandom()%100000 + 1
	if loser == winner {
		loser = winner%100000 + 1
	}
	return [2]int64{winner, loser}
}

func main() {
	tournaments := make([][][2]int64, 4)
	for t := range tournaments {
		tournaments[t] = make([][2]int64, 100000)
		for i := range tournaments[t] {
			tournaments[t][i] = drawMatch()
		}
	}
	var listed, check int64
	for r := 0; r < 25; r++ {
		for t := 0; t < 4; t++ {
			// punch: one match is drawn again before each answer
			at := wideRandom() % 100000
			tournaments[t][at] = drawMatch()
			for _, list := range findWinners(tournaments[t]) {
				listed += int64(len(list))
				check = (check*31 + int64(len(list))) % 1000000007
				for _, p := range list {
					check = (check*31 + p) % 1000000007
				}
			}
		}
	}
	fmt.Printf("100 tournaments: %d players listed in all, checksum %d\n", listed, check)
}
