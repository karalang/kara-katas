// LeetCode #1366 bench -- Go: how many votes put each team in each place
// counted, and the teams sorted by those counts, then by letter.
package main

import (
	"fmt"
	"sort"
)

func rankTeams(votes []string) string {
	places := len(votes[0])
	counts := make([][]int64, 26)
	for t := range counts {
		counts[t] = make([]int64, places)
	}
	for _, vote := range votes {
		for place := 0; place < places; place++ {
			counts[vote[place]-'A'][place]++
		}
	}
	teams := []byte(votes[0])
	sort.Slice(teams, func(x, y int) bool {
		a, b := counts[teams[x]-'A'], counts[teams[y]-'A']
		for p := range a {
			if a[p] != b[p] {
				return a[p] > b[p]
			}
		}
		return teams[x] < teams[y]
	})
	return string(teams)
}

var seed int64 = 1366

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 20 elections of 1000 votes over all 26 teams, the constraints' most,
	// built once; then 3000 rounds, each swapping two places of one vote,
	// all drawn from the checksum so far, ranking that election and
	// folding the ranking into the checksum
	elections := make([][]string, 20)
	for e := range elections {
		votes := make([]string, 1000)
		for v := range votes {
			vote := []byte("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
			for i := int64(1); i < 26; i++ {
				j := nextRandom() % (i + 1)
				vote[i], vote[j] = vote[j], vote[i]
			}
			votes[v] = string(vote)
		}
		elections[e] = votes
	}
	var check int64
	for r := int64(0); r < 3000; r++ {
		e, v := check%20, (check/20)%1000
		i, j := (check/20000)%26, (check/520000)%26
		vote := []byte(elections[e][v])
		vote[i], vote[j] = vote[j], vote[i]
		elections[e][v] = string(vote)
		ranked := rankTeams(elections[e])
		for k := 0; k < len(ranked); k++ {
			check = (check*31 + int64(ranked[k])) % 1000000007
		}
		check = (check + r) % 1000000007
	}
	fmt.Printf("3000 rounds over 20 elections of 1000 votes: checksum %d\n", check)
}
