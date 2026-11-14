// LeetCode #2157: Groups of Strings -- the benchmark's Go mirror of
// groups.kara.
package main

import (
	"fmt"
	"strings"
)

func find(parent []int64, x int64) int64 {
	for parent[x] != x {
		parent[x] = parent[parent[x]]
		x = parent[x]
	}
	return x
}

func unite(parent, size []int64, a, b int64) {
	ra := find(parent, a)
	rb := find(parent, b)
	if ra == rb {
		return
	}
	big, small := ra, rb
	if size[ra] < size[rb] {
		big, small = rb, ra
	}
	parent[small] = big
	size[big] += size[small]
}

func groupStrings(words []string) []int64 {
	n := len(words)
	masks := make([]int64, n)
	for i, w := range words {
		for j := 0; j < len(w); j++ {
			masks[i] |= 1 << (w[j] - 'a')
		}
	}
	parent := make([]int64, n)
	size := make([]int64, n)
	for i := range parent {
		parent[i] = int64(i)
		size[i] = 1
	}
	first := map[int64]int64{}
	for i := 0; i < n; i++ {
		if j, ok := first[masks[i]]; ok {
			unite(parent, size, int64(i), j)
		} else {
			first[masks[i]] = int64(i)
		}
	}
	blanked := map[int64]int64{}
	for i := 0; i < n; i++ {
		for bit := 0; bit < 26; bit++ {
			if (masks[i]>>bit)&1 == 1 {
				less := masks[i] ^ (1 << bit)
				if j, ok := first[less]; ok {
					unite(parent, size, int64(i), j)
				}
				if j, ok := blanked[less]; ok {
					unite(parent, size, int64(i), j)
				} else {
					blanked[less] = int64(i)
				}
			}
		}
	}
	var groups, largest int64
	for i := 0; i < n; i++ {
		if find(parent, int64(i)) == int64(i) {
			groups++
			if size[i] > largest {
				largest = size[i]
			}
		}
	}
	return []int64{groups, largest}
}

var seed int64 = 2157

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func word() string {
	length := int(nextRandom()%8 + 1)
	w := ""
	for len(w) < length {
		c := string(rune('a' + nextRandom()%20))
		if !strings.Contains(w, c) {
			w += c
		}
	}
	return w
}

func main() {
	lists := make([][]string, 4)
	for l := range lists {
		lists[l] = make([]string, 5000)
		for i := range lists[l] {
			lists[l][i] = word()
		}
	}
	var total, check int64
	for round := int64(0); round < 25; round++ {
		for l := 0; l < 4; l++ {
			at := nextRandom() % 5000
			lists[l][at] = word()
			answer := groupStrings(lists[l])
			total += answer[0]
			check = (check*31 + answer[0]*10007 + answer[1] + round) % 1000000007
		}
	}
	fmt.Printf("100 solves: %d groups in all, checksum %d\n", total, check)
}
