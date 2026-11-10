// LeetCode #2092: Find All People With Secret -- Go mirror of the ★ arm's
// benchmark (secret.kara): the same 10 gatherings, each answered 4 times by
// the same stable sort and union-find over slices.
package main

import (
	"fmt"
	"sort"
)

var seed int64 = 2092

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type meeting struct{ x, y, t int64 }

func find(parent []int64, x int64) int64 {
	for parent[x] != x {
		parent[x] = parent[parent[x]]
		x = parent[x]
	}
	return x
}

func findAllPeople(n int64, meetings []meeting, first int64) []int64 {
	s := append([]meeting(nil), meetings...)
	sort.SliceStable(s, func(i, j int) bool { return s[i].t < s[j].t })
	parent := make([]int64, n)
	for p := range parent {
		parent[p] = int64(p)
	}
	parent[first] = 0
	i := 0
	for i < len(s) {
		j := i
		for j < len(s) && s[j].t == s[i].t {
			rx, ry := find(parent, s[j].x), find(parent, s[j].y)
			if rx < ry {
				parent[ry] = rx
			} else {
				parent[rx] = ry
			}
			j++
		}
		for k := i; k < j; k++ {
			if find(parent, s[k].x) != 0 {
				parent[s[k].x] = s[k].x
			}
			if find(parent, s[k].y) != 0 {
				parent[s[k].y] = s[k].y
			}
		}
		i = j
	}
	var knows []int64
	for p := int64(0); p < n; p++ {
		if find(parent, p) == 0 {
			knows = append(knows, p)
		}
	}
	return knows
}

func main() {
	const n = 100000
	gatherings := make([][]meeting, 10)
	for g := range gatherings {
		ms := make([]meeting, 0, 100000)
		for k := 0; k < 100000; k++ {
			x := (nextRandom()*32768 + nextRandom()) % n
			y := (x + 1 + (nextRandom()*32768+nextRandom())%(n-1)) % n
			ms = append(ms, meeting{x, y, nextRandom()%1000 + 1})
		}
		gatherings[g] = ms
	}
	var total, check int64
	for round := int64(0); round < 4; round++ {
		for g := int64(0); g < 10; g++ {
			got := findAllPeople(n, gatherings[g], round*10+g+1)
			total += int64(len(got))
			for _, p := range got {
				check = (check*31 + p) % 1000000007
			}
		}
	}
	fmt.Printf("40 answers: %d people, checksum %d\n", total, check)
}
