package main

import "fmt"

func numIslands(grid []int64, rows, cols int64) int64 {
	var count int64 = 0
	for r := int64(0); r < rows; r++ {
		for c := int64(0); c < cols; c++ {
			if grid[r*cols+c] == 1 {
				count++
				stack := []int64{r*cols + c}
				grid[r*cols+c] = 0
				for len(stack) > 0 {
					idx := stack[len(stack)-1]
					stack = stack[:len(stack)-1]
					cr := idx / cols
					cc := idx % cols
					if cr > 0 && grid[(cr-1)*cols+cc] == 1 {
						grid[(cr-1)*cols+cc] = 0
						stack = append(stack, (cr-1)*cols+cc)
					}
					if cr+1 < rows && grid[(cr+1)*cols+cc] == 1 {
						grid[(cr+1)*cols+cc] = 0
						stack = append(stack, (cr+1)*cols+cc)
					}
					if cc > 0 && grid[cr*cols+(cc-1)] == 1 {
						grid[cr*cols+(cc-1)] = 0
						stack = append(stack, cr*cols+(cc-1))
					}
					if cc+1 < cols && grid[cr*cols+(cc+1)] == 1 {
						grid[cr*cols+(cc+1)] = 0
						stack = append(stack, cr*cols+(cc+1))
					}
				}
			}
		}
	}
	return count
}

func main() {
	var rows int64 = 80
	var cols int64 = 80
	var passes int64 = 13000
	total := rows * cols

	master := make([]int64, total)
	var state int64 = 12345
	for g := int64(0); g < total; g++ {
		state = (state*1103515245 + 12345) & 2147483647
		if (state>>16)%100 < 45 {
			master[g] = 1
		} else {
			master[g] = 0
		}
	}

	work := make([]int64, total)
	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		state = (state*1103515245 + 12345) & 2147483647
		idx := state % total
		master[idx] = 1 - master[idx]
		copy(work, master)
		sink += numIslands(work, rows, cols)
	}
	fmt.Println(sink)
}
