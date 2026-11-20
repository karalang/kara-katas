// LeetCode #1728: Cat and Mouse II -- the bench (mouse.kara): the game
// solved backwards from its ends, a state lost for the player to move
// once every move from it is counted off.
package main

import "fmt"

func reach(marks [][]byte, at, jump int) []int {
	rows, cols := len(marks), len(marks[0])
	r, c := at/cols, at%cols
	cells := []int{at}
	for _, d := range [4][2]int{{0, 1}, {1, 0}, {0, -1}, {-1, 0}} {
		for k := 1; k <= jump; k++ {
			nr, nc := r+d[0]*k, c+d[1]*k
			if nr < 0 || nr >= rows || nc < 0 || nc >= cols || marks[nr][nc] == '#' {
				break
			}
			cells = append(cells, nr*cols+nc)
		}
	}
	return cells
}

func canMouseWin(grid []string, catJump, mouseJump int) bool {
	marks := make([][]byte, len(grid))
	for i, row := range grid {
		marks[i] = []byte(row)
	}
	cols := len(marks[0])
	cells := len(marks) * cols
	mouse, cat, food := 0, 0, 0
	for at := 0; at < cells; at++ {
		switch marks[at/cols][at%cols] {
		case 'M':
			mouse = at
		case 'C':
			cat = at
		case 'F':
			food = at
		}
	}
	open := make([]bool, cells)
	mouseMoves := make([][]int, cells)
	catMoves := make([][]int, cells)
	for at := 0; at < cells; at++ {
		open[at] = marks[at/cols][at%cols] != '#'
		if open[at] {
			mouseMoves[at] = reach(marks, at, mouseJump)
			catMoves[at] = reach(marks, at, catJump)
		}
	}
	state := func(m, c, turn int) int { return (m*cells+c)*2 + turn }
	result := make([]int, cells*cells*2)
	left := make([]int, cells*cells*2)
	queue := make([]int, 0, cells*cells*2)
	for m := 0; m < cells; m++ {
		for c := 0; c < cells; c++ {
			if !open[m] || !open[c] {
				continue
			}
			left[state(m, c, 0)] = len(mouseMoves[m])
			left[state(m, c, 1)] = len(catMoves[c])
			end := 0
			if m == c || c == food {
				end = 2
			} else if m == food {
				end = 1
			}
			if end != 0 {
				for turn := 0; turn < 2; turn++ {
					result[state(m, c, turn)] = end
					queue = append(queue, state(m, c, turn))
				}
			}
		}
	}
	for head := 0; head < len(queue); head++ {
		s := queue[head]
		turn, m, c := s%2, s/2/cells, s/2%cells
		won := result[s]
		if turn == 0 {
			for _, before := range catMoves[c] {
				p := state(m, before, 1)
				if result[p] != 0 {
					continue
				}
				if won == 2 {
					result[p] = 2
					queue = append(queue, p)
				} else {
					left[p]--
					if left[p] == 0 {
						result[p] = 1
						queue = append(queue, p)
					}
				}
			}
		} else {
			for _, before := range mouseMoves[m] {
				p := state(before, c, 0)
				if result[p] != 0 {
					continue
				}
				if won == 1 {
					result[p] = 1
					queue = append(queue, p)
				} else {
					left[p]--
					if left[p] == 0 {
						result[p] = 2
						queue = append(queue, p)
					}
				}
			}
		}
	}
	return result[state(mouse, cat, 0)] == 1
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

type problem struct {
	grid               []string
	catJump, mouseJump int
}

func main() {
	count := 200
	var rounds int64 = 20
	side := 8
	cells := side * side
	var seed int64 = 1728
	problems := make([]problem, count)
	for p := range problems {
		marks := make([]byte, cells)
		for i := range marks {
			if nextRandom(&seed)%4 == 0 {
				marks[i] = '#'
			} else {
				marks[i] = '.'
			}
		}
		places := make([]int, cells)
		for i := range places {
			places[i] = i
		}
		for i := 0; i < 3; i++ {
			j := i + int(nextRandom(&seed)%int64(cells-i))
			places[i], places[j] = places[j], places[i]
		}
		marks[places[0]] = 'C'
		marks[places[1]] = 'M'
		marks[places[2]] = 'F'
		grid := make([]string, side)
		for r := 0; r < side; r++ {
			grid[r] = string(marks[r*side : (r+1)*side])
		}
		catJump := int(nextRandom(&seed)%int64(side) + 1)
		mouseJump := int(nextRandom(&seed)%int64(side) + 1)
		problems[p] = problem{grid, catJump, mouseJump}
	}
	var wins, check int64
	for r := int64(0); r < rounds; r++ {
		for _, pr := range problems {
			answer := canMouseWin(pr.grid, pr.catJump, pr.mouseJump)
			var bit int64 = 1
			if answer {
				wins++
				bit = 2
			}
			check = (check*31 + bit + r) % 1000000007
		}
	}
	fmt.Printf("%d grids of %d by %d, %d rounds: the mouse wins %d, checksum %d\n", count, side, side, rounds, wins, check)
}
