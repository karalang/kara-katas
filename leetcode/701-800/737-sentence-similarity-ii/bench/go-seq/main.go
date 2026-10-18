// LeetCode #737: Sentence Similarity II -- union-find.
// Benchmark mirror of the Kara star arm: number every word in a pair,
// join the two words of each pair in a union-find with union by size
// and path compression, and compare the roots of the two words at each
// place.
package main

import "fmt"

func find(parent []int64, x int64) int64 {
	root := x
	for parent[root] != root {
		root = parent[root]
	}
	for parent[x] != root {
		next := parent[x]
		parent[x] = root
		x = next
	}
	return root
}

func areSentencesSimilarTwo(sentence1, sentence2 []string, pairs [][2]string) bool {
	if len(sentence1) != len(sentence2) {
		return false
	}
	ids := map[string]int64{}
	var parent, size []int64
	number := func(w string) int64 {
		if i, ok := ids[w]; ok {
			return i
		}
		i := int64(len(parent))
		ids[w] = i
		parent = append(parent, i)
		size = append(size, 1)
		return i
	}
	for _, p := range pairs {
		a := number(p[0])
		b := number(p[1])
		ra, rb := find(parent, a), find(parent, b)
		if ra != rb {
			if size[ra] < size[rb] {
				parent[ra] = rb
				size[rb] += size[ra]
			} else {
				parent[rb] = ra
				size[ra] += size[rb]
			}
		}
	}
	for i := range sentence1 {
		if sentence1[i] == sentence2[i] {
			continue
		}
		a, ok1 := ids[sentence1[i]]
		b, ok2 := ids[sentence2[i]]
		if !ok1 || !ok2 || find(parent, a) != find(parent, b) {
			return false
		}
	}
	return true
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(737)
	var pairs [][2]string
	near := make([][]int64, 3000)
	for k := 0; k < 2000; k++ {
		a := nextRandom(&seed) % 3000
		b := nextRandom(&seed) % 3000
		pairs = append(pairs, [2]string{fmt.Sprintf("w%d", a), fmt.Sprintf("w%d", b)})
		near[a] = append(near[a], b)
		near[b] = append(near[b], a)
	}
	var s1, s2 []string
	for k := 0; k < 1000; k++ {
		start := nextRandom(&seed) % 3000
		at := start
		steps := nextRandom(&seed) % 6
		for t := int64(0); t < steps; t++ {
			if len(near[at]) > 0 {
				at = near[at][nextRandom(&seed)%int64(len(near[at]))]
			}
		}
		s1 = append(s1, fmt.Sprintf("w%d", start))
		s2 = append(s2, fmt.Sprintf("w%d", at))
	}
	similar := 0
	for r := 0; r < 1000; r++ {
		j := nextRandom(&seed) % 1000
		x := nextRandom(&seed) % 3000
		saved := s2[j]
		s2[j] = fmt.Sprintf("w%d", x)
		if areSentencesSimilarTwo(s1, s2, pairs) {
			similar++
		}
		s2[j] = saved
		if areSentencesSimilarTwo(s1, s2, pairs) {
			similar++
		}
	}
	fmt.Printf("1000 rounds of 2 checks of 1000 words with 2000 pairs: %d similar\n", similar)
}
