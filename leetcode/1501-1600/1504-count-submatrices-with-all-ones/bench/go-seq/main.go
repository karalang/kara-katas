// LeetCode #1504: Count Submatrices With All Ones -- the benchmark, the
// same algorithm as submat.kara: column heights per row and a stack of
// increasing heights.
package main

import "fmt"

func countSubmatrices(mat [][]int64) int64 {
	m, n := len(mat), len(mat[0])
	heights := make([]int64, n)
	var total int64
	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			if mat[i][j] == 1 {
				heights[j]++
			} else {
				heights[j] = 0
			}
		}
		ending := make([]int64, n)
		stack := []int{}
		for j := 0; j < n; j++ {
			for len(stack) > 0 && heights[stack[len(stack)-1]] >= heights[j] {
				stack = stack[:len(stack)-1]
			}
			if len(stack) == 0 {
				ending[j] = heights[j] * int64(j+1)
			} else {
				k := stack[len(stack)-1]
				ending[j] = ending[k] + heights[j]*int64(j-k)
			}
			stack = append(stack, j)
			total += ending[j]
		}
	}
	return total
}

var seed int64 = 1504

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func randomSquare(size, ones int64) [][]int64 {
	mat := make([][]int64, size)
	for r := range mat {
		mat[r] = make([]int64, size)
		for c := range mat[r] {
			if nextRandom()%100 < ones {
				mat[r][c] = 1
			}
		}
	}
	return mat
}

func main() {
	mats := make([][][]int64, 400)
	for i := range mats {
		mats[i] = randomSquare(150, int64(50+i%50))
	}
	var total, check int64
	for _, mat := range mats {
		answer := countSubmatrices(mat)
		total += answer
		check = mix(check, answer)
	}
	fmt.Printf("400 matrices of 150 x 150: sum %d, checksum %d\n", total, check)
}
