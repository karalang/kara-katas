// LeetCode #1178: Number of Valid Words for Each Puzzle -- the ★ arm's
// bench in Go: each word's letter set counted in a map, each puzzle's
// subsets of its other six letters walked with `sub = (sub - 1) & rest`.
// The same words, the same puzzles and the same 20 calls.
package main

import "fmt"

func findNumOfValidWords(words []string, puzzles []string) []int64 {
	count := map[int64]int64{}
	for _, w := range words {
		mask := int64(0)
		for i := 0; i < len(w); i++ {
			mask |= 1 << (w[i] - 'a')
		}
		count[mask]++
	}
	answer := make([]int64, 0, len(puzzles))
	for _, p := range puzzles {
		first := int64(1) << (p[0] - 'a')
		rest := int64(0)
		for i := 1; i < len(p); i++ {
			rest |= 1 << (p[i] - 'a')
		}
		total := int64(0)
		sub := rest
		for {
			total += count[sub|first]
			if sub == 0 {
				break
			}
			sub = (sub - 1) & rest
		}
		answer = append(answer, total)
	}
	return answer
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func distinct(seed *int64, m, k int64) []byte {
	letters := make([]byte, m)
	for i := int64(0); i < m; i++ {
		letters[i] = byte('a' + i)
	}
	for i := int64(0); i < k; i++ {
		j := i + nextRandom(seed)%(m-i)
		letters[i], letters[j] = letters[j], letters[i]
	}
	return letters[:k]
}

func main() {
	seed := int64(1178)
	words := make([]string, 0, 100000)
	for i := 0; i < 100000; i++ {
		k := 1 + nextRandom(&seed)%7
		set := distinct(&seed, 14, k)
		n := 4 + nextRandom(&seed)%47
		w := make([]byte, n)
		for j := range w {
			w[j] = set[nextRandom(&seed)%int64(len(set))]
		}
		words = append(words, string(w))
	}
	puzzles := make([]string, 10000)
	for i := range puzzles {
		puzzles[i] = string(distinct(&seed, 14, 7))
	}
	calls := 20
	check := int64(0)
	for c := 0; c < calls; c++ {
		for _, a := range findNumOfValidWords(words, puzzles) {
			check = (check*131 + a + 1) % 1000000007
		}
	}
	fmt.Printf("%d calls: checksum %d\n", calls, check)
}
