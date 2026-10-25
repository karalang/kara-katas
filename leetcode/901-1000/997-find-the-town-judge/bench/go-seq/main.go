// Benchmark: LeetCode #997 Find the Town Judge -- the ★ arm, one score
// per person, on random towns of 1000 people and 10000 trusts,
// LeetCode's largest. Mirrors find_judge.kara, .c, .rs and .py.
package main

import "fmt"

func findJudge(n int64, trust [][]int64) int64 {
	score := make([]int64, n+1)
	for _, t := range trust {
		score[t[0]]--
		score[t[1]]++
	}
	for person := int64(1); person <= n; person++ {
		if score[person] == n-1 {
			return person
		}
	}
	return -1
}

var seed int64 = 997

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

// 1000 people and 10000 different trusts: in even towns 999 of them are
// everyone else trusting a judge, and the rest are at random
func randomTown(a int) [][]int64 {
	var pairs [][]int64
	seen := make([]bool, 2000*1001)
	var judge int64
	if a%2 == 0 {
		judge = 1 + nextRandom()%1000
		for p := int64(1); p <= 1000; p++ {
			if p != judge {
				seen[p*2000+judge] = true
				pairs = append(pairs, []int64{p, judge})
			}
		}
	}
	for len(pairs) < 10000 {
		x := 1 + nextRandom()%1000
		y := 1 + nextRandom()%1000
		if x != y && x != judge && !seen[x*2000+y] {
			seen[x*2000+y] = true
			pairs = append(pairs, []int64{x, y})
		}
	}
	return pairs
}

func main() {
	rounds := 1000
	towns := make([][][]int64, 20)
	for a := range towns {
		towns[a] = randomTown(a)
	}
	var judges, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 20; i++ {
			got := findJudge(1000, towns[(r+i)%20])
			if got > 0 {
				judges++
			}
			check = (check*31 + got + 2) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 20 towns of 1000 people: %d judges, checksum %d\n", rounds, judges, check)
}
