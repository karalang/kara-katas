// Benchmark: LeetCode #963 Minimum Area Rectangle II -- the ★ arm,
// diagonals grouped by centre, on 50 points, LeetCode's largest, packed
// into small grids so that many pairs share a centre and a length. Each
// call first moves one point to a free spot. Mirrors
// ../min_area_free_rect.kara, .c, .rs and .py.
package main

import "fmt"

var seed int64 = 963

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type pair struct{ i, j int }

func minAreaFreeRect(points [][2]int64) float64 {
	n := len(points)
	groups := map[[3]int64][]pair{}
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			dx := points[i][0] - points[j][0]
			dy := points[i][1] - points[j][1]
			key := [3]int64{points[i][0] + points[j][0], points[i][1] + points[j][1], dx*dx + dy*dy}
			groups[key] = append(groups[key], pair{i, j})
		}
	}
	var best int64
	for _, pairs := range groups {
		for x := 0; x < len(pairs); x++ {
			for y := x + 1; y < len(pairs); y++ {
				i := pairs[x].i
				k, l := pairs[y].i, pairs[y].j
				ux := points[k][0] - points[i][0]
				uy := points[k][1] - points[i][1]
				vx := points[l][0] - points[i][0]
				vy := points[l][1] - points[i][1]
				area := ux*vy - uy*vx
				if area < 0 {
					area = -area
				}
				if best == 0 || area < best {
					best = area
				}
			}
		}
	}
	return float64(best)
}

func has(points [][2]int64, x, y int64) bool {
	for _, p := range points {
		if p[0] == x && p[1] == y {
			return true
		}
	}
	return false
}

func packed(n int, top int64) [][2]int64 {
	var out [][2]int64
	for len(out) < n {
		x := nextRandom() % (top + 1)
		y := nextRandom() % (top + 1)
		if !has(out, x, y) {
			out = append(out, [2]int64{x, y})
		}
	}
	return out
}

func main() {
	rounds := 40
	cases := make([][][2]int64, 50)
	for i := range cases {
		cases[i] = packed(50, int64(7+i%10))
	}
	total := 0.0
	var check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 50; i++ {
			c := (r + i) % 50
			top := int64(7 + c%10)
			p := nextRandom() % 50
			x := nextRandom() % (top + 1)
			y := nextRandom() % (top + 1)
			if !has(cases[c], x, y) {
				cases[c][p] = [2]int64{x, y}
			}
			a := minAreaFreeRect(cases[c])
			total += a
			check = (check*31 + int64(a) + int64(i)) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 50 cases of 50 points: the areas sum to %.5f, checksum %d\n", rounds, total, check)
}
