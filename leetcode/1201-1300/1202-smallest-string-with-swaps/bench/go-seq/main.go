// LeetCode #1202 bench, in Go: the ★ arm (a union-find over the indices,
// path halving and union by size; each group's letters, sorted, go back to
// its indices in rising order) on one string of 100000 random letters and
// four sets of pairs drawn once, then 10 rounds over the four, each answer
// folded into a checksum.
package main

import (
	"fmt"
	"slices"
)

var seed int64 = 1202

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func find(parent []int, x int) int {
	for parent[x] != x {
		parent[x] = parent[parent[x]]
		x = parent[x]
	}
	return x
}

func smallestStringWithSwaps(s []byte, pairs [][2]int) []byte {
	n := len(s)
	parent := make([]int, n)
	size := make([]int, n)
	for i := range parent {
		parent[i] = i
		size[i] = 1
	}
	for _, p := range pairs {
		a, b := find(parent, p[0]), find(parent, p[1])
		if a != b {
			if size[a] < size[b] {
				a, b = b, a
			}
			parent[b] = a
			size[a] += size[b]
		}
	}
	groups := make([][]int, n)
	for i := 0; i < n; i++ {
		r := find(parent, i)
		groups[r] = append(groups[r], i)
	}
	out := slices.Clone(s)
	for _, g := range groups {
		letters := make([]byte, len(g))
		for k, i := range g {
			letters[k] = s[i]
		}
		slices.Sort(letters)
		for k, i := range g {
			out[i] = letters[k]
		}
	}
	return out
}

func randomPairs(n, m int) [][2]int {
	pairs := make([][2]int, 0, m)
	for p := 0; p < m; p++ {
		hi := nextRandom()
		a := int((hi*32768 + nextRandom()) % int64(n))
		hi = nextRandom()
		b := int((hi*32768 + nextRandom()) % int64(n))
		pairs = append(pairs, [2]int{a, b})
	}
	return pairs
}

func main() {
	n := 100000
	s := make([]byte, n)
	for i := range s {
		s[i] = byte('a' + nextRandom()%26)
	}
	sets := [][][2]int{randomPairs(n, 25000), randomPairs(n, 100000), nil, nil}
	for i := 0; i < n-2; i++ {
		sets[2] = append(sets[2], [2]int{i, i + 2})
	}
	for i := 0; i < n-1000; i++ {
		sets[3] = append(sets[3], [2]int{i, i + 1000})
	}
	var check int64
	for round := 0; round < 10; round++ {
		for _, pairs := range sets {
			t := smallestStringWithSwaps(s, pairs)
			for _, b := range t {
				check = (check*131 + int64(b)) % 1000000007
			}
		}
	}
	fmt.Printf("10 rounds over 4 sets of pairs on 100000 letters: checksum %d\n", check)
}
