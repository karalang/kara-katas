// LeetCode #1010 bench: the ★ arm (remainder counts in one pass) over 20
// playlists of 60,000 songs, drawn once; each of 250 rounds counts the
// pairs of every playlist, starting from a different one, and folds each
// count into a checksum.
package main

import "fmt"

func numPairs(time []int64) int64 {
	var seen [60]int64
	var pairs int64
	for _, t := range time {
		r := t % 60
		pairs += seen[(60-r)%60]
		seen[r]++
	}
	return pairs
}

var seed int64 = 1010

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count, rounds := 20, 250
	playlists := make([][]int64, count)
	for k := range playlists {
		playlists[k] = make([]int64, 60000)
		for i := range playlists[k] {
			playlists[k][i] = 1 + nextRandom()%500
		}
	}
	var check int64
	for r := 0; r < rounds; r++ {
		for k := 0; k < count; k++ {
			check = (check*31 + numPairs(playlists[(r+k)%count])) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d playlists of 60000 songs: checksum %d\n", rounds, count, check)
}
