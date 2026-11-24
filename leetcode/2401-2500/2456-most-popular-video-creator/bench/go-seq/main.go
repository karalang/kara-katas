// LeetCode #2456: Most Popular Video Creator -- bench, Go mirror of
// creator.kara: one pass keeps each creator's total and best video in a
// map, then every creator at the largest total, sorted.
package main

import (
	"fmt"
	"sort"
)

type stat struct {
	total, top int64
	id         string
}

func mostPopularCreator(creators, ids []string, views []int64) [][]string {
	stats := map[string]stat{}
	for i := range creators {
		c := creators[i]
		if s, ok := stats[c]; ok {
			better := views[i] > s.top || (views[i] == s.top && ids[i] < s.id)
			if better {
				stats[c] = stat{s.total + views[i], views[i], ids[i]}
			} else {
				stats[c] = stat{s.total + views[i], s.top, s.id}
			}
		} else {
			stats[c] = stat{views[i], views[i], ids[i]}
		}
	}
	var most int64
	for _, s := range stats {
		if s.total > most {
			most = s.total
		}
	}
	answer := [][]string{}
	for c, s := range stats {
		if s.total == most {
			answer = append(answer, []string{c, s.id})
		}
	}
	sort.Slice(answer, func(a, b int) bool {
		if answer[a][0] != answer[b][0] {
			return answer[a][0] < answer[b][0]
		}
		return answer[a][1] < answer[b][1]
	})
	return answer
}

var seed int64 = 2456

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomName(length, letters int64) string {
	b := make([]byte, length)
	for i := range b {
		b[i] = byte(97 + nextRandom()%letters)
	}
	return string(b)
}

func main() {
	type list struct {
		creators, ids []string
		views         []int64
	}
	lists := make([]list, 10)
	for a := range lists {
		creators := make([]string, 100000)
		for i := range creators {
			creators[i] = randomName(3, 26)
		}
		ids := make([]string, 100000)
		for i := range ids {
			ids[i] = randomName(5, 26)
		}
		views := make([]int64, 100000)
		for i := range views {
			views[i] = nextRandom() % 100001
		}
		lists[a] = list{creators, ids, views}
	}
	var check int64
	for p := int64(0); p < 16; p++ {
		for a := int64(0); a < 10; a++ {
			lists[a].views[(p*7919+a)%100000] = check % 100001
			for _, pair := range mostPopularCreator(lists[a].creators, lists[a].ids, lists[a].views) {
				for _, w := range pair {
					for i := 0; i < len(w); i++ {
						check = (check*31 + int64(w[i])) % 1000000007
					}
				}
			}
			check = (check + p) % 1000000007
		}
	}
	fmt.Printf("16 passes over 10 lists of 10^5 videos: checksum %d\n", check)
}
