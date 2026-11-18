// LeetCode #1620: Coordinate With Maximum Network Quality -- the bench in Go,
// mirroring network.kara: every point, every tower, f64 distances.
package main

import (
	"fmt"
	"math"
)

func bestCoordinate(towers [][]int32, radius int32) []int32 {
	best := []int32{0, 0}
	var most int32
	for x := int32(0); x <= 50; x++ {
		for y := int32(0); y <= 50; y++ {
			var quality int32
			for _, t := range towers {
				dx, dy := t[0]-x, t[1]-y
				d := math.Sqrt(float64(dx*dx + dy*dy))
				if d <= float64(radius) {
					quality += int32(math.Floor(float64(t[2]) / (1.0 + d)))
				}
			}
			if quality > most {
				most = quality
				best = []int32{x, y}
			}
		}
	}
	return best
}

var seed int64 = 1620

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	type kase struct {
		towers [][]int32
		radius int32
	}
	cases := make([]kase, 1000)
	for c := range cases {
		towers := make([][]int32, 50)
		for i := range towers {
			x := int32(nextRandom() % 51)
			y := int32(nextRandom() % 51)
			q := int32(nextRandom() % 51)
			towers[i] = []int32{x, y, q}
		}
		cases[c] = kase{towers, int32(nextRandom()%50 + 1)}
	}
	var check, spread int64
	for _, k := range cases {
		best := bestCoordinate(k.towers, k.radius)
		spread += int64(best[0] + best[1])
		check = (check*31 + int64(best[0]*51+best[1]) + 1) % 1000000007
	}
	fmt.Printf("1000 cases of 50 towers: coordinates sum to %d, checksum %d\n", spread, check)
}
