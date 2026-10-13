// Benchmark for #488: Go mirror of the ★ arm (breadth first); see
// ../zuma_game.kara.
package main

import (
	"fmt"
	"sort"
)

func shrink(board []byte) []byte {
	b := board
	for {
		kept := []byte{}
		removed := false
		i := 0
		for i < len(b) {
			j := i
			for j < len(b) && b[j] == b[i] {
				j++
			}
			if j-i >= 3 {
				removed = true
			} else {
				kept = append(kept, b[i:j]...)
			}
			i = j
		}
		b = kept
		if !removed {
			return b
		}
	}
}

func findMinStep(board, hand string) int64 {
	first := []byte(hand)
	sort.Slice(first, func(x, y int) bool { return first[x] < first[y] })
	boards := [][]byte{[]byte(board)}
	hands := [][]byte{first}
	seen := map[string]struct{}{}
	var steps int64
	for len(boards) > 0 {
		steps++
		nextBoards := [][]byte{}
		nextHands := [][]byte{}
		for s := range boards {
			b := boards[s]
			h := hands[s]
			for t := 0; t < len(h); t++ {
				c := h[t]
				if t > 0 && h[t-1] == c {
					continue
				}
				for i := 0; i <= len(b); i++ {
					startsRun := i < len(b) && b[i] == c && (i == 0 || b[i-1] != c)
					splitsPair := i > 0 && i < len(b) && b[i-1] == b[i] && b[i] != c
					if !startsRun && !splitsPair {
						continue
					}
					inserted := make([]byte, 0, len(b)+1)
					inserted = append(inserted, b[:i]...)
					inserted = append(inserted, c)
					inserted = append(inserted, b[i:]...)
					after := shrink(inserted)
					if len(after) == 0 {
						return steps
					}
					rest := make([]byte, 0, len(h)-1)
					rest = append(rest, h[:t]...)
					rest = append(rest, h[t+1:]...)
					state := string(after) + "|" + string(rest)
					if _, ok := seen[state]; !ok {
						seen[state] = struct{}{}
						nextBoards = append(nextBoards, after)
						nextHands = append(nextHands, rest)
					}
				}
			}
		}
		boards = nextBoards
		hands = nextHands
	}
	return -1
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	colours := []byte("RYBGW")
	boards := []string{}
	hands := []string{}
	var seed int64 = 488
	for c := int64(0); c < 60; c++ {
		palette := 2 + c%3
		balls := []byte{}
		for len(balls) < 16 {
			ball := colours[nextRandom(&seed)%palette]
			n := len(balls)
			if n >= 2 && balls[n-1] == ball && balls[n-2] == ball {
				continue
			}
			balls = append(balls, ball)
		}
		boards = append(boards, string(balls))
		hand := []byte{}
		for i := 0; i < 5; i++ {
			hand = append(hand, colours[nextRandom(&seed)%palette])
		}
		hands = append(hands, string(hand))
	}
	var cleared, total, checksum int64
	for k := range boards {
		steps := findMinStep(boards[k], hands[k])
		if steps >= 0 {
			cleared++
			total += steps
		}
		checksum = (checksum*31 + steps + 2) % 1000000007
	}
	fmt.Printf("60 cases of 16 balls and a hand of 5: %d cleared with %d balls, checksum %d\n", cleared, total, checksum)
}
