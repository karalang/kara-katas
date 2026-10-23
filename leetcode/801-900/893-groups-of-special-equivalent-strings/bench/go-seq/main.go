// LeetCode #893 bench: Go mirror of num_special_equiv_groups.kara (the
// union-find arm, every pair of words compared by their counts of letters
// at even and at odd positions) on the same 300 lists of 1000 words.
package main

import "fmt"

func numSpecialEquivGroups(words []string) int64 {
	n := len(words)
	counts := make([][52]int64, n)
	for w, word := range words {
		for i := 0; i < len(word); i++ {
			counts[w][int(word[i]-97)+26*(i%2)]++
		}
	}
	parent := make([]int, n)
	for i := range parent {
		parent[i] = i
	}
	find := func(x int) int {
		for parent[x] != x {
			parent[x] = parent[parent[x]]
			x = parent[x]
		}
		return x
	}
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			if counts[i] == counts[j] {
				a, b := find(i), find(j)
				if a != b {
					parent[a] = b
				}
			}
		}
	}
	var groups int64
	for i := 0; i < n; i++ {
		if find(i) == i {
			groups++
		}
	}
	return groups
}

var seed int64 = 893

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(length, letters int64) string {
	w := make([]byte, length)
	for i := range w {
		w[i] = byte(97 + nextRandom()%letters)
	}
	return string(w)
}

func shuffled(word string) string {
	b := []byte(word)
	n := int64(len(b))
	for s := int64(0); s < n; s++ {
		i := nextRandom() % n
		j := nextRandom() % n
		if i%2 == j%2 {
			b[i], b[j] = b[j], b[i]
		}
	}
	return string(b)
}

func main() {
	var groups, check int64
	for c := 0; c < 300; c++ {
		words := make([]string, 0, 1000)
		for w := 0; w < 1000; w++ {
			if len(words) > 0 && nextRandom()%2 == 0 {
				k := nextRandom() % int64(len(words))
				words = append(words, shuffled(words[k]))
			} else {
				words = append(words, randomWord(20, 26))
			}
		}
		got := numSpecialEquivGroups(words)
		groups += got
		check = (check*131 + got) % 1000000007
	}
	fmt.Printf("300 lists of 1000 words of 20 letters: %d groups, checksum %d\n", groups, check)
}
