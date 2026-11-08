// LeetCode #1515 bench: the ★ arm's ternary search twice, as centre.kara.
package main

import (
	"fmt"
	"math"
)

type point struct{ x, y int64 }

func cost(positions []point, x, y float64) float64 {
	total := 0.0
	for _, p := range positions {
		dx := float64(p.x) - x
		dy := float64(p.y) - y
		total += math.Sqrt(dx*dx + dy*dy)
	}
	return total
}

func bestOn(positions []point, x float64) float64 {
	lo, hi := 0.0, 100.0
	for r := 0; r < 60; r++ {
		m1 := lo + (hi-lo)/3.0
		m2 := hi - (hi-lo)/3.0
		if cost(positions, x, m1) < cost(positions, x, m2) {
			hi = m2
		} else {
			lo = m1
		}
	}
	return cost(positions, x, (lo+hi)/2.0)
}

func getMinDistSum(positions []point) float64 {
	lo, hi := 0.0, 100.0
	for r := 0; r < 60; r++ {
		m1 := lo + (hi-lo)/3.0
		m2 := hi - (hi-lo)/3.0
		if bestOn(positions, m1) < bestOn(positions, m2) {
			hi = m2
		} else {
			lo = m1
		}
	}
	return bestOn(positions, (lo+hi)/2.0)
}

var seed int64 = 1515

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var check int64
	for s := 0; s < 100; s++ {
		positions := make([]point, 0, 50)
		for i := 0; i < 50; i++ {
			x := nextRandom() % 101
			y := nextRandom() % 101
			positions = append(positions, point{x, y})
		}
		answer := getMinDistSum(positions)
		check = (check*31 + int64(math.Floor(answer*100.0+0.5)) + 1) % 1000000007
	}
	fmt.Printf("100 sets of 50 customers on 0..100: checksum %d\n", check)
}
