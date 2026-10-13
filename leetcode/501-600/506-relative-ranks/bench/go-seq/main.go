// Benchmark for #506 in Go: the ★ arm (the athletes sorted by score);
// see ../../find_relative_ranks.kara. A stable sort of the indices by
// score, highest first, and a fresh string for every rank.
package main

import (
	"fmt"
	"slices"
	"strconv"
)

func findRelativeRanks(score []int64) []string {
	n := len(score)
	order := make([]int, n)
	for i := range order {
		order[i] = i
	}
	slices.SortStableFunc(order, func(a, b int) int {
		x, y := -score[a], -score[b]
		if x < y {
			return -1
		}
		if x > y {
			return 1
		}
		return 0
	})
	answer := make([]string, n)
	for place := 0; place < n; place++ {
		switch place {
		case 0:
			answer[order[place]] = "Gold Medal"
		case 1:
			answer[order[place]] = "Silver Medal"
		case 2:
			answer[order[place]] = "Bronze Medal"
		default:
			answer[order[place]] = strconv.Itoa(place + 1)
		}
	}
	return answer
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 500 lists of 10,000 athletes (the problem's most), all different
	// scores from 0 to 10^6 (the j-th is j * 100 plus less than 100,
	// shuffled), built once. Then each list is ranked once, the length
	// of every rank folded into a checksum.
	lists := 500
	n := int64(10000)
	seed := int64(506)
	var all [][]int64
	for c := 0; c < lists; c++ {
		score := make([]int64, 0, n)
		for j := int64(0); j < n; j++ {
			score = append(score, j*100+nextRandom(&seed)%100)
		}
		for k := n - 1; k > 0; k-- {
			other := nextRandom(&seed) % (k + 1)
			score[k], score[other] = score[other], score[k]
		}
		all = append(all, score)
	}
	var letters, checksum int64
	for c := 0; c < lists; c++ {
		for _, rank := range findRelativeRanks(all[c]) {
			letters += int64(len(rank))
			checksum = (checksum*31 + int64(len(rank))) % 1000000007
		}
	}
	fmt.Printf("%d lists of %d athletes: %d characters, checksum %d\n", lists, n, letters, checksum)
}
