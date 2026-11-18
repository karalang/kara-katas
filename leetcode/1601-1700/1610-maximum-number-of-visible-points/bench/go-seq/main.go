// LeetCode #1610: Maximum Number of Visible Points -- the bench in Go,
// mirroring visible.kara: each direction in degrees (`atan2` times
// 180 / pi, as Rust's `to_degrees`), sorted and doubled with 360 more, and
// a window slid along it.
package main

import (
	"fmt"
	"math"
	"slices"
)

func visiblePoints(points [][2]int32, angle int, location [2]int32) int {
	toDegrees := 180.0 / math.Pi
	here := 0
	dirs := make([]float64, 0, 2*len(points))
	for _, p := range points {
		dx, dy := p[0]-location[0], p[1]-location[1]
		if dx == 0 && dy == 0 {
			here++
		} else {
			dirs = append(dirs, math.Atan2(float64(dy), float64(dx))*toDegrees)
		}
	}
	slices.Sort(dirs)
	m := len(dirs)
	for i := 0; i < m; i++ {
		dirs = append(dirs, dirs[i]+360.0)
	}
	reach := float64(angle) + 1e-9
	best, j := 0, 0
	for i := range dirs {
		for dirs[i]-dirs[j] > reach {
			j++
		}
		if i-j+1 > best {
			best = i - j + 1
		}
	}
	return best + here
}

func main() {
	seed := int64(1610)
	nextRandom := func() int64 {
		seed = (seed*1103515245 + 12345) % 2147483648
		return seed / 65536
	}
	type problem struct {
		points   [][2]int32
		angle    int
		location [2]int32
	}
	var problems []problem
	for p := 0; p < 20; p++ {
		points := make([][2]int32, 0, 100000)
		for i := 0; i < 100000; i++ {
			x := int32(nextRandom() % 101)
			y := int32(nextRandom() % 101)
			points = append(points, [2]int32{x, y})
		}
		angle := int(nextRandom() % 360)
		lx := int32(nextRandom() % 101)
		ly := int32(nextRandom() % 101)
		problems = append(problems, problem{points, angle, [2]int32{lx, ly}})
	}
	var check, visible int64
	for _, pr := range problems {
		v := int64(visiblePoints(pr.points, pr.angle, pr.location))
		check = (check*31 + v + 1) % 1000000007
		visible += v
	}
	fmt.Printf("20 problems of 100000 points from 0 to 100: %d visible, checksum %d\n", visible, check)
}
