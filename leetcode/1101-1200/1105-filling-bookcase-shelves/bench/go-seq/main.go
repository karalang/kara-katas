// LeetCode #1105: Filling Bookcase Shelves -- the bench in Go: the ★ arm
// (the least height for the first i books over every run ending at book
// i that fits a shelf) over 32 bookcases of 1000 books, each round
// changing one book in every bookcase and solving it again.
package main

import (
	"fmt"
	"math"
)

func minHeightShelves(books [][]int64, shelfWidth int64) int64 {
	n := len(books)
	best := make([]int64, n+1)
	for i := 1; i <= n; i++ {
		var width, tallest int64
		best[i] = math.MaxInt64
		j := i
		for j > 0 && width+books[j-1][0] <= shelfWidth {
			width += books[j-1][0]
			if books[j-1][1] > tallest {
				tallest = books[j-1][1]
			}
			if best[j-1]+tallest < best[i] {
				best[i] = best[j-1] + tallest
			}
			j--
		}
	}
	return best[n]
}

var seed int64 = 1105

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	cases := make([][][]int64, 0, 32)
	for c := 0; c < 32; c++ {
		books := make([][]int64, 1000)
		for i := range books {
			t := nextRandom()%50 + 1
			books[i] = []int64{t, nextRandom()%1000 + 1}
		}
		cases = append(cases, books)
	}
	var total, check int64
	for round := int64(0); round < 200; round++ {
		for j := range cases {
			at := (round*7919 + int64(j)*104729) % 1000
			cases[j][at][0] = (cases[j][at][0]*7+round)%50 + 1
			cases[j][at][1] = (cases[j][at][1]*13+int64(j))%1000 + 1
			h := minHeightShelves(cases[j], 1000)
			total += h
			check = (check*31 + h) % 1000000007
		}
	}
	fmt.Printf("200 rounds over 32 bookcases of 1000 books: heights total %d, checksum %d\n", total, check)
}
