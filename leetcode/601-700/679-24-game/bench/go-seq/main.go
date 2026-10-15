// Benchmark for #679: the ★ arm, pairs combined in floating point.
package main

import (
	"fmt"
	"math"
)

func reach(values []float64) bool {
	n := len(values)
	if n == 1 {
		return math.Abs(values[0]-24.0) < 0.000001
	}
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			a, b := values[i], values[j]
			rest := []float64{}
			for k := 0; k < n; k++ {
				if k != i && k != j {
					rest = append(rest, values[k])
				}
			}
			results := []float64{a + b, a - b, b - a, a * b}
			if b != 0.0 {
				results = append(results, a/b)
			}
			if a != 0.0 {
				results = append(results, b/a)
			}
			for _, r := range results {
				next := append(append([]float64{}, rest...), r)
				if reach(next) {
					return true
				}
			}
		}
	}
	return false
}

func judgePoint24(cards []int64) bool {
	values := make([]float64, len(cards))
	for i, c := range cards {
		values[i] = float64(c)
	}
	return reach(values)
}

func main() {
	solvable, sum := int64(0), int64(0)
	for a := int64(1); a < 14; a++ {
		for b := int64(1); b < 14; b++ {
			for c := int64(1); c < 14; c++ {
				for d := int64(1); d < 14; d++ {
					code := a*1000 + b*100 + c*10 + d
					if judgePoint24([]int64{a, b, c, d}) {
						solvable++
						sum = (sum*31 + code) % 1000000007
					} else {
						sum = (sum*31 + 7) % 1000000007
					}
				}
			}
		}
	}
	fmt.Printf("28561 hands: %d solvable, checksum %d\n", solvable, sum)
}
