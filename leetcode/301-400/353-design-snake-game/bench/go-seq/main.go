// Bench mirror of snake_game.kara (the grid + ring-buffer arm), same algorithm.
package main

import "fmt"

const (
	rounds = 30
	width  = 1000
	height = 400
)

type point struct{ r, c int64 }

type snakeGame struct {
	width, height int64
	food          []point
	nextFood      int64
	ring          []int64
	start, length int64
	covered       []bool
}

func newGame(w, h int64, food []point) *snakeGame {
	cap := w * h
	g := &snakeGame{width: w, height: h, food: food, ring: make([]int64, cap), length: 1, covered: make([]bool, cap)}
	g.covered[0] = true
	return g
}

func (g *snakeGame) step(dir byte) int64 {
	cap := int64(len(g.ring))
	head := g.ring[(g.start+g.length-1)%cap]
	r, c := head/g.width, head%g.width
	switch dir {
	case 'U':
		r--
	case 'D':
		r++
	case 'L':
		c--
	default:
		c++
	}
	if r < 0 || r >= g.height || c < 0 || c >= g.width {
		return -1
	}
	cell := r*g.width + c
	if g.nextFood < int64(len(g.food)) && g.food[g.nextFood] == (point{r, c}) {
		g.nextFood++
	} else {
		g.covered[g.ring[g.start]] = false
		g.start = (g.start + 1) % cap
		g.length--
	}
	if g.covered[cell] {
		return -1
	}
	g.ring[(g.start+g.length)%cap] = cell
	g.length++
	g.covered[cell] = true
	return g.nextFood
}

func main() {
	var sink int64
	for round := int64(0); round < rounds; round++ {
		w, h := int64(width), int64(height+2*round)
		n := w * h
		moves := make([]byte, 0, n)
		for i := int64(0); i < w-1; i++ {
			moves = append(moves, 'R')
		}
		for row := int64(1); row < h; row++ {
			moves = append(moves, 'D')
			d := byte('R')
			if row%2 == 1 {
				d = 'L'
			}
			for i := int64(0); i < w-2; i++ {
				moves = append(moves, d)
			}
		}
		moves = append(moves, 'L')
		for i := int64(0); i < h-1; i++ {
			moves = append(moves, 'U')
		}
		var food []point
		var r, c int64
		for t := int64(0); int64(len(food)) < n/4; t++ {
			switch moves[t] {
			case 'U':
				r--
			case 'D':
				r++
			case 'L':
				c--
			default:
				c++
			}
			if t%3 == 2 {
				food = append(food, point{r, c})
			}
		}
		g := newGame(w, h, food)
		for t := int64(0); t < 3*n; t++ {
			s := g.step(moves[t%n])
			sink = (sink*31 + s + t) % 1000000007
		}
		sink = (sink + g.length) % 1000000007
	}
	fmt.Println(sink)
}
