// LeetCode #1779: Find Nearest Point That Has the Same X or Y Coordinate --
// the bench in Go, mirroring nearest_valid_point.kara: one pass keeping the
// nearest valid point so far.
package main

import (
	"fmt"
	"math"
)

func abs(v int32) int32 {
	if v < 0 {
		return -v
	}
	return v
}

func nearestValidPoint(x, y int32, points [][]int32) int32 {
	best := int32(-1)
	nearest := int32(math.MaxInt32)
	for i := 0; i < len(points); i++ {
		a, b := points[i][0], points[i][1]
		if a == x || b == y {
			d := abs(a-x) + abs(b-y)
			if d < nearest {
				nearest = d
				best = int32(i)
			}
		}
	}
	return best
}

var seed int64 = 1779

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][][]int32, 0, 20)
	for l := 0; l < 20; l++ {
		points := make([][]int32, 0, 10000)
		for k := 0; k < 10000; k++ {
			a := 1 + nextRandom()%100
			b := 1 + nextRandom()%100
			points = append(points, []int32{int32(a), int32(b)})
		}
		lists = append(lists, points)
	}
	var check int64
	for call := int64(0); call < 20000; call++ {
		x := 1 + (check+call)%100
		y := 1 + (check/100+call*7)%100
		found := nearestValidPoint(int32(x), int32(y), lists[call%20])
		check = (check*31 + int64(found) + 1) % 1000000007
	}
	fmt.Printf("20000 calls over 20 lists: checksum %d\n", check)
}
