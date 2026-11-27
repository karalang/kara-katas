// LeetCode #1828: Queries on Number of Points Inside a Circle -- the bench in
// Go: the ★ arm over 200 calls on runs of 250 to 499 points and 250 to 499
// queries cut from one list of 1000 points and one of 1000 queries of radius 1
// to 500, built once, each run's start and lengths drawn from the checksum so
// far. Each call copies its runs, as the arm takes its lists by value.
package main

import "fmt"

func countPoints(points [][]int64, queries [][]int64) []int64 {
	answer := make([]int64, 0, len(queries))
	for _, q := range queries {
		x, y, r := q[0], q[1], q[2]
		var inside int64
		for _, p := range points {
			dx, dy := p[0]-x, p[1]-y
			if dx*dx+dy*dy <= r*r {
				inside++
			}
		}
		answer = append(answer, inside)
	}
	return answer
}

var seed int64 = 1828

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

// a copy of rows, each row its own slice, as the arm takes its lists by value
func copyRows(rows [][]int64) [][]int64 {
	out := make([][]int64, len(rows))
	for i, row := range rows {
		out[i] = append([]int64(nil), row...)
	}
	return out
}

func main() {
	points := make([][]int64, 0, 1000)
	for i := 0; i < 1000; i++ {
		x := nextRandom() % 501
		points = append(points, []int64{x, nextRandom() % 501})
	}
	queries := make([][]int64, 0, 1000)
	for i := 0; i < 1000; i++ {
		x := nextRandom() % 501
		y := nextRandom() % 501
		queries = append(queries, []int64{x, y, 1 + nextRandom()%500})
	}
	var check int64
	for call := int64(0); call < 200; call++ {
		from := (check + call) % 500
		n := 250 + (check*7+call)%250
		m := 250 + (check*13+call)%250
		answer := countPoints(copyRows(points[from:from+n]), copyRows(queries[from:from+m]))
		for _, c := range answer {
			check = (check*31 + c) % 1000000007
		}
	}
	fmt.Printf("200 calls: checksum %d\n", check)
}
