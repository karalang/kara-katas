// LeetCode #692: Top K Frequent Words -- bench program, Go mirror of the select arm.
package main

import (
	"fmt"
	"sort"
)

var seed int64 = 692

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func topKFrequent(words []string, k int) []string {
	sorted := append([]string(nil), words...)
	sort.Strings(sorted)
	distinct := []string{}
	counts := []int64{}
	for i := 0; i < len(sorted); {
		j := i
		for j < len(sorted) && sorted[j] == sorted[i] {
			j++
		}
		distinct = append(distinct, sorted[i])
		counts = append(counts, int64(j-i))
		i = j
	}
	out := []string{}
	for r := 0; r < k; r++ {
		pick := -1
		for d := range distinct {
			if counts[d] > 0 && (pick < 0 || counts[d] > counts[pick]) {
				pick = d
			}
		}
		out = append(out, distinct[pick])
		counts[pick] = 0
	}
	return out
}

func main() {
	lists := [][]string{}
	for l := 0; l < 100; l++ {
		words := []string{}
		for i := 0; i < 500; i++ {
			n := 1 + nextRandom()%4
			w := make([]byte, n)
			for c := range w {
				w[c] = byte('a' + nextRandom()%6)
			}
			words = append(words, string(w))
		}
		lists = append(lists, words)
	}
	rounds := 60
	var checksum, answers int64
	for r := 0; r < rounds; r++ {
		for _, words := range lists {
			for _, w := range topKFrequent(words, 10) {
				for i := 0; i < len(w); i++ {
					checksum = (checksum*31 + int64(w[i])) % 1000000007
				}
				checksum = (checksum*31 + 1) % 1000000007
				answers++
			}
		}
	}
	fmt.Printf("%d rounds of 100 lists of 500 words: %d words answered, checksum %d\n", rounds, answers, checksum)
}
