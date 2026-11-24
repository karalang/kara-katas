// LeetCode #1311 bench, Go: the ★ arm (a breadth-first walk a level at a
// time, the videos of the people left counted in a map, then sorted as
// (count, title) pairs) on the same 50 groups and 200 passes.
package main

import (
	"fmt"
	"sort"
)

type ranked struct {
	count int64
	title string
}

func watchedVideosByFriends(watchedVideos [][]string, friends [][]int64, id, level int64) []string {
	seen := make([]bool, len(friends))
	seen[id] = true
	people := []int64{id}
	for l := int64(0); l < level; l++ {
		var next []int64
		for _, p := range people {
			for _, f := range friends[p] {
				if !seen[f] {
					seen[f] = true
					next = append(next, f)
				}
			}
		}
		people = next
	}
	count := map[string]int64{}
	for _, p := range people {
		for _, video := range watchedVideos[p] {
			count[video]++
		}
	}
	pairs := make([]ranked, 0, len(count))
	for video, c := range count {
		pairs = append(pairs, ranked{c, video})
	}
	sort.Slice(pairs, func(i, j int) bool {
		if pairs[i].count != pairs[j].count {
			return pairs[i].count < pairs[j].count
		}
		return pairs[i].title < pairs[j].title
	})
	out := make([]string, len(pairs))
	for i, r := range pairs {
		out[i] = r.title
	}
	return out
}

var seed int64 = 1311

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func fold(check int64, title string) int64 {
	for _, ch := range title {
		check = (check*31 + int64(ch)) % 1000000007
	}
	return check
}

func main() {
	letters := "abcdefghijklmnopqrstuvwxyz"
	titles := make([]string, 0, 400)
	for t := 0; t < 400; t++ {
		length := 1 + nextRandom()%8
		b := make([]byte, 0, length)
		for k := int64(0); k < length; k++ {
			b = append(b, letters[nextRandom()%26])
		}
		titles = append(titles, string(b))
	}
	const n = 100
	groups := make([][][]string, 50)
	links := make([][][]int64, 50)
	for g := 0; g < 50; g++ {
		friends := make([][]int64, n)
		for a := int64(0); a < n; a++ {
			for b := a + 1; b < n; b++ {
				if nextRandom()%25 == 0 {
					friends[a] = append(friends[a], b)
					friends[b] = append(friends[b], a)
				}
			}
		}
		watched := make([][]string, n)
		for p := 0; p < n; p++ {
			videos := make([]string, 100)
			for k := range videos {
				videos[k] = titles[nextRandom()%400]
			}
			watched[p] = videos
		}
		groups[g] = watched
		links[g] = friends
	}
	var check int64
	for pass := int64(0); pass < 200; pass++ {
		for g := 0; g < 50; g++ {
			groups[g][check%n][(check/7)%100] = titles[(check/11)%400]
			id := (check / 13) % n
			level := 1 + (check/17)%3
			got := watchedVideosByFriends(groups[g], links[g], id, level)
			check = (check*31 + int64(len(got))) % 1000000007
			if len(got) > 0 {
				check = fold(check, got[0])
				check = fold(check, got[len(got)-1])
			}
			check = (check + pass) % 1000000007
		}
	}
	fmt.Printf("200 passes over 50 groups of 100: checksum %d\n", check)
}
