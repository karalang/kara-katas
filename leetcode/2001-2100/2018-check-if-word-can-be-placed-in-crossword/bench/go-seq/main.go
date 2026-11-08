// LeetCode #2018: Check if Word Can Be Placed In Crossword -- the ★ arm's
// benchmark, a mirror of crossword.kara: the lines built and each run
// collected into its own slice per call.
package main

import "fmt"

func fits(segment, word []rune) bool {
	k := len(word)
	if len(segment) != k {
		return false
	}
	forward, backward := true, true
	for i := 0; i < k && forward; i++ {
		forward = segment[i] == ' ' || segment[i] == word[i]
	}
	for i := 0; i < k && backward; i++ {
		backward = segment[i] == ' ' || segment[i] == word[k-1-i]
	}
	return forward || backward
}

func placeWordInCrossword(board [][]rune, w string) bool {
	word := []rune(w)
	m, n := len(board), len(board[0])
	lines := make([][]rune, 0, m+n)
	for _, row := range board {
		lines = append(lines, append([]rune(nil), row...))
	}
	for c := 0; c < n; c++ {
		col := make([]rune, 0)
		for r := 0; r < m; r++ {
			col = append(col, board[r][c])
		}
		lines = append(lines, col)
	}
	for _, line := range lines {
		segment := make([]rune, 0)
		for i := 0; i < len(line)+1; i++ {
			if i == len(line) || line[i] == '#' {
				if fits(segment, word) {
					return true
				}
				segment = segment[:0]
			} else {
				segment = append(segment, line[i])
			}
		}
	}
	return false
}

var seed int64 = 2018

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	boards := make([][][]rune, 0, 120)
	words := make([]string, 0, 120)
	for b := int64(0); b < 120; b++ {
		walls := b%2 + 1
		board := make([][]rune, 0, 200)
		for r := 0; r < 200; r++ {
			row := make([]rune, 0)
			for c := 0; c < 200; c++ {
				if nextRandom()%10 < walls {
					row = append(row, '#')
				} else if nextRandom()%10 < 4 {
					row = append(row, rune('a'+nextRandom()%3))
				} else {
					row = append(row, ' ')
				}
			}
			board = append(board, row)
		}
		word := make([]rune, 0)
		for i := int64(0); i < b%10+10; i++ {
			word = append(word, rune('a'+nextRandom()%3))
		}
		boards = append(boards, board)
		words = append(words, string(word))
	}
	var calls, placed, check int64
	for round := 0; round < 40; round++ {
		for b := range boards {
			answer := placeWordInCrossword(boards[b], words[b])
			calls++
			bit := int64(0)
			if answer {
				placed++
				bit = 1
			}
			check = (check*2 + bit) % 1000000007
		}
	}
	fmt.Printf("%d calls: %d placed, checksum %d\n", calls, placed, check)
}
