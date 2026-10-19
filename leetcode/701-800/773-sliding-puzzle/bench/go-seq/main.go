// LeetCode 773 — Sliding Puzzle: benchmark, the ★ arm in Go.
// All 720 boards, in dictionary order, built once; ROUNDS rounds each
// solve the next of them.
package main

import "fmt"

const ROUNDS = 20000

var neighbours = [][]int{{1, 3}, {0, 2, 4}, {1, 5}, {0, 4}, {1, 3, 5}, {2, 4}}

type item struct {
	state string
	steps int64
}

func slidingPuzzle(board [][]int64) int64 {
	b := make([]byte, 0, 6)
	for _, row := range board {
		for _, x := range row {
			b = append(b, byte(48+x))
		}
	}
	start := string(b)
	seen := map[string]bool{start: true}
	queue := []item{{start, 0}}
	for head := 0; head < len(queue); head++ {
		it := queue[head]
		if it.state == "123450" {
			return it.steps
		}
		bytes := []byte(it.state)
		zero := 0
		for bytes[zero] != '0' {
			zero++
		}
		for _, next := range neighbours[zero] {
			moved := make([]byte, 6)
			copy(moved, bytes)
			moved[zero], moved[next] = moved[next], moved[zero]
			text := string(moved)
			if !seen[text] {
				seen[text] = true
				queue = append(queue, item{text, it.steps + 1})
			}
		}
	}
	return -1
}

func nextOrder(cells []int64) bool {
	i := len(cells) - 2
	for i >= 0 && cells[i] >= cells[i+1] {
		i--
	}
	if i < 0 {
		return false
	}
	j := len(cells) - 1
	for cells[j] <= cells[i] {
		j--
	}
	cells[i], cells[j] = cells[j], cells[i]
	for lo, hi := i+1, len(cells)-1; lo < hi; lo, hi = lo+1, hi-1 {
		cells[lo], cells[hi] = cells[hi], cells[lo]
	}
	return true
}

func main() {
	var boards [][][]int64
	cells := []int64{0, 1, 2, 3, 4, 5}
	for {
		boards = append(boards, [][]int64{{cells[0], cells[1], cells[2]}, {cells[3], cells[4], cells[5]}})
		if !nextOrder(cells) {
			break
		}
	}
	var solved, check int64
	for round := 0; round < ROUNDS; round++ {
		answer := slidingPuzzle(boards[round%720])
		if answer >= 0 {
			solved++
		}
		check = (check*31 + answer + 1) % 1000000007
	}
	fmt.Printf("%d boards: %d solvable, checksum %d\n", ROUNDS, solved, check)
}
