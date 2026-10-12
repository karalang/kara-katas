// Benchmark for #451: mirror of frequency_sort.kara (count, then sort
// the distinct characters) on 20 random strings of 200,000 characters,
// built once, then each sorted 5 times.
package main

import (
	"fmt"
	"sort"
	"strings"
)

type entry struct {
	negative int64
	c        rune
}

func frequencySort(s string) string {
	counts := map[rune]int64{}
	for _, c := range s {
		counts[c]++
	}
	order := []entry{}
	for c, n := range counts {
		order = append(order, entry{-n, c})
	}
	sort.Slice(order, func(i, j int) bool {
		if order[i].negative != order[j].negative {
			return order[i].negative < order[j].negative
		}
		return order[i].c < order[j].c
	})
	var out strings.Builder
	for _, e := range order {
		for i := int64(0); i < -e.negative; i++ {
			out.WriteRune(e.c)
		}
	}
	return out.String()
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	alphabet := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	const count, n, rounds = 20, 200000, 5
	sizes := []int64{3, 10, 30, 62}
	seed := int64(451)
	strs := []string{}
	for i := 0; i < count; i++ {
		// From the first 3, 10, 30 or all 62 characters, in turn.
		k := sizes[i%4]
		var s strings.Builder
		for j := 0; j < n; j++ {
			s.WriteByte(alphabet[nextRandom(&seed)%k])
		}
		strs = append(strs, s.String())
	}
	characters, checksum := int64(0), int64(0)
	for r := 0; r < rounds; r++ {
		for _, s := range strs {
			out := frequencySort(s)
			length := int64(len(out))
			characters += length
			sample := int64(out[0])*65536 + int64(out[len(out)/2])*256 + int64(out[len(out)-1])
			checksum = (checksum*31 + length + sample) % 1000000007
		}
	}
	fmt.Printf("%d rounds on %d strings of %d: %d characters, checksum %d\n", rounds, count, n, characters, checksum)
}
