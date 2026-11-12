// LeetCode #1128: Number of Equivalent Domino Pairs -- the bench in Go, the
// ★ arm over LeetCode's `[][]int` with an array of 100 counts, the same 16
// sets and 300 rounds.
package main

import "fmt"

func numEquivDominoPairs(dominoes [][]int) int64 {
	var count [100]int64
	var pairs int64
	for _, d := range dominoes {
		lo, hi := min(d[0], d[1]), max(d[0], d[1])
		key := lo*10 + hi
		pairs += count[key]
		count[key]++
	}
	return pairs
}

var seed int64 = 1128

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	sets := make([][][]int, 0, 16)
	for s := 0; s < 16; s++ {
		dominoes := make([][]int, 0, 40000)
		for i := 0; i < 40000; i++ {
			a := nextRandom()%9 + 1
			b := nextRandom()%9 + 1
			dominoes = append(dominoes, []int{int(a), int(b)})
		}
		sets = append(sets, dominoes)
	}
	var total, check int64
	for round := int64(0); round < 300; round++ {
		for j := int64(0); j < int64(len(sets)); j++ {
			at := (round*7919 + j*104729) % 40000
			side := round % 2
			sets[j][at][side] = sets[j][at][side]%9 + 1
			answer := numEquivDominoPairs(sets[j])
			total += answer
			check = (check*31 + answer) % 1000000007
		}
	}
	fmt.Printf("300 rounds over 16 sets of 4 * 10^4 dominoes: pairs total %d, checksum %d\n", total, check)
}
