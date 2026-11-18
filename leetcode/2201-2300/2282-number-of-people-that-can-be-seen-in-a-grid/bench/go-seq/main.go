// LeetCode #2282: Number of People That Can Be Seen in a Grid -- the
// bench, the ★ arm.
package main

import "fmt"

// how many each person in `line` sees farther along it
func sightings(line []int64) []int64 {
	seen := make([]int64, len(line))
	stack := make([]int64, 0)
	for i := len(line) - 1; i >= 0; i-- {
		h := line[i]
		for len(stack) > 0 && stack[len(stack)-1] < h {
			stack = stack[:len(stack)-1]
			seen[i]++
		}
		if len(stack) > 0 {
			seen[i]++
			if stack[len(stack)-1] == h {
				stack = stack[:len(stack)-1]
			}
		}
		stack = append(stack, h)
	}
	return seen
}

func seePeople(heights [][]int64) [][]int64 {
	m, n := len(heights), len(heights[0])
	answer := make([][]int64, 0, m)
	for i := 0; i < m; i++ {
		answer = append(answer, sightings(heights[i]))
	}
	for j := 0; j < n; j++ {
		column := make([]int64, m)
		for i := 0; i < m; i++ {
			column[i] = heights[i][j]
		}
		down := sightings(column)
		for i := 0; i < m; i++ {
			answer[i][j] += down[i]
		}
	}
	return answer
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2282

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var check int64
	for t := 0; t < 40; t++ {
		heights := make([][]int64, 0, 400)
		for i := 0; i < 400; i++ {
			row := make([]int64, 0, 400)
			for j := 0; j < 400; j++ {
				top := nextRandom()
				row = append(row, (top*32768+nextRandom())%100000+1)
			}
			heights = append(heights, row)
		}
		answer := seePeople(heights)
		var seen int64
		for _, row := range answer {
			for _, a := range row {
				seen += a
			}
		}
		check = (check*31 + seen) % 1000000007
	}
	fmt.Printf("40 grids of 400 by 400: checksum %d\n", check)
}
