// Benchmark for #839: Similar String Groups -- the ★ arm (union-find).
//
// Mirrors similar_string_groups.kara: every pair of words is compared
// once, stopping at a third difference, and a pair that differs in no
// position or in two joins its two groups, kept as a union-find forest
// with path halving. As in the Kāra program, each word is copied out to
// its own slice for every count.
package main

import "fmt"

func similar(a, b []byte) bool {
	diff := 0
	for k := 0; k < len(a); k++ {
		if a[k] != b[k] {
			diff++
			if diff > 2 {
				return false
			}
		}
	}
	return diff != 1
}

func find(parent []int64, x int64) int64 {
	v := x
	for parent[v] != v {
		parent[v] = parent[parent[v]]
		v = parent[v]
	}
	return v
}

func numSimilarGroups(strs []string) int64 {
	words := make([][]byte, len(strs))
	for i, s := range strs {
		words[i] = []byte(s)
	}
	n := int64(len(words))
	parent := make([]int64, n)
	for i := range parent {
		parent[i] = int64(i)
	}
	groups := n
	for i := int64(0); i < n; i++ {
		for j := i + 1; j < n; j++ {
			a := find(parent, i)
			b := find(parent, j)
			if a != b && similar(words[i], words[j]) {
				parent[a] = b
				groups--
			}
		}
	}
	return groups
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 16 cases drawn once, each LeetCode's most and longest words, 300 of
	// 300 letters. The first word of case g is random; each later one is
	// an earlier word with one swap, or with three once in 1 + g % 4
	// words. Each round counts the groups of the next case.
	const count, rounds, n, m = 16, 500, 300, 300
	seed := int64(839)
	cases := make([][]string, 0, count)
	for g := int64(0); g < count; g++ {
		jump := 1 + g%4
		words := [][]byte{}
		first := make([]byte, 0, m)
		for k := 0; k < m; k++ {
			first = append(first, byte(97+nextRandom(&seed)%26))
		}
		words = append(words, first)
		for i := 1; i < n; i++ {
			from := nextRandom(&seed) % int64(len(words))
			swaps := 1
			if nextRandom(&seed)%jump == 0 {
				swaps = 3
			}
			w := append([]byte(nil), words[from]...)
			for s := 0; s < swaps; s++ {
				p := nextRandom(&seed) % m
				q := nextRandom(&seed) % m
				w[p], w[q] = w[q], w[p]
			}
			words = append(words, w)
		}
		strs := make([]string, len(words))
		for i, w := range words {
			strs[i] = string(w)
		}
		cases = append(cases, strs)
	}
	total, checksum := int64(0), int64(0)
	for round := int64(0); round < rounds; round++ {
		groups := numSimilarGroups(cases[round%count])
		total += groups
		checksum = (checksum*31 + groups + round) % 1000000007
	}
	fmt.Printf("%d rounds of %d cases: %d groups, checksum %d\n", rounds, count, total, checksum)
}
