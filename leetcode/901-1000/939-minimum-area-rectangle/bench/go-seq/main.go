// Benchmark: LeetCode #939 Minimum Area Rectangle -- the ★ arm, pairs as
// diagonals, on 20 sets of 500 points, LeetCode's most, in 10 rounds.
// Mirrors min_area_rect.kara, .c, .rs and .py.
package main

import "fmt"

func abs(v int64) int64 {
	if v < 0 {
		return -v
	}
	return v
}

func minAreaRect(points [][2]int64) int64 {
	seen := make(map[int64]struct{}, len(points))
	for _, p := range points {
		seen[p[0]*40001+p[1]] = struct{}{}
	}
	var best int64
	n := len(points)
	for i := 0; i < n; i++ {
		x1, y1 := points[i][0], points[i][1]
		for j := i + 1; j < n; j++ {
			x2, y2 := points[j][0], points[j][1]
			if x1 != x2 && y1 != y2 {
				if _, ok := seen[x1*40001+y2]; !ok {
					continue
				}
				if _, ok := seen[x2*40001+y1]; !ok {
					continue
				}
				area := abs(x1-x2) * abs(y1-y2)
				if best == 0 || area < best {
					best = area
				}
			}
		}
	}
	return best
}

var seed int64 = 939

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds, count := 10, 20
	sets := make([][][2]int64, 0, count)
	for s := 0; s < count; s++ {
		step := 1 + nextRandom()%100
		ox := nextRandom() % 1000
		oy := nextRandom() % 1000
		taken := make([]bool, 1600)
		points := make([][2]int64, 0, 500)
		for len(points) < 500 {
			hi := nextRandom()
			c := (hi*32768 + nextRandom()) % 1600
			if !taken[c] {
				taken[c] = true
				points = append(points, [2]int64{ox + (c%40)*step, oy + (c/40)*step})
			}
		}
		sets = append(sets, points)
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			a := minAreaRect(sets[(r+i)%count])
			total += a
			check = (check*1000003 + a) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d sets of 500 points: areas adding to %d, checksum %d\n", rounds, count, total, check)
}
