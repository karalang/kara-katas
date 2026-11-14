// LeetCode #1152 bench -- mirrors most_visited_pattern.kara: the same
// 64 problems, the same rounds, the ★ arm's maps and sets.
package main

import (
	"fmt"
	"sort"
)

type tri [3]string

func less(p, q tri) bool {
	for i := 0; i < 3; i++ {
		if p[i] != q[i] {
			return p[i] < q[i]
		}
	}
	return false
}

func mostVisitedPattern(username []string, timestamp []int64, website []string) []string {
	order := make([]int, len(username))
	for i := range order {
		order[i] = i
	}
	sort.SliceStable(order, func(a, b int) bool { return timestamp[order[a]] < timestamp[order[b]] })
	byUser := map[string][]string{}
	for _, i := range order {
		byUser[username[i]] = append(byUser[username[i]], website[i])
	}
	score := map[tri]int64{}
	for _, sites := range byUser {
		n := len(sites)
		seen := map[tri]struct{}{}
		for a := 0; a < n; a++ {
			for b := a + 1; b < n; b++ {
				for c := b + 1; c < n; c++ {
					seen[tri{sites[a], sites[b], sites[c]}] = struct{}{}
				}
			}
		}
		for p := range seen {
			score[p] = score[p] + 1
		}
	}
	var best tri
	var top int64 = -1
	for p, s := range score {
		if s > top || (s == top && less(p, best)) {
			best, top = p, s
		}
	}
	return []string{best[0], best[1], best[2]}
}

var seed int64 = 1152

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type problem struct {
	username  []string
	timestamp []int64
	website   []string
}

func main() {
	rounds := 5000
	siteNames := make([]string, 8)
	for s := range siteNames {
		siteNames[s] = fmt.Sprintf("site%d", s)
	}
	problems := []problem{}
	for p := 0; p < 64; p++ {
		username := make([]string, 50)
		for i := range username {
			username[i] = fmt.Sprintf("user%d", nextRandom()%5)
		}
		website := make([]string, 50)
		for i := range website {
			website[i] = siteNames[nextRandom()%8]
		}
		timestamp := make([]int64, 50)
		for i := range timestamp {
			timestamp[i] = int64(i + 1)
		}
		for j := 49; j >= 1; j-- {
			k := nextRandom() % int64(j+1)
			timestamp[j], timestamp[k] = timestamp[k], timestamp[j]
		}
		problems = append(problems, problem{username, timestamp, website})
	}
	distinct := 0
	var check int64
	for r := 0; r < rounds; r++ {
		p := r % 64
		for q := 0; q < 4; q++ {
			at := nextRandom() % 50
			problems[p].website[at] = siteNames[nextRandom()%8]
		}
		a := mostVisitedPattern(problems[p].username, problems[p].timestamp, problems[p].website)
		if a[0] != a[1] && a[1] != a[2] && a[0] != a[2] {
			distinct++
		}
		for _, w := range a {
			for _, c := range []byte(w) {
				check = (check*31 + int64(c)) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds over 64 problems of 50 visits: %d patterns of three sites, checksum %d\n", rounds, distinct, check)
}
