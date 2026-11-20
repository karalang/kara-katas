// LeetCode #2326: Spiral Matrix IV -- the bench, the ★ arm in Go. A
// walker starts at the top left heading right and writes the list's
// values one by one, turning clockwise when the next cell is off the grid
// or already written. O(m n).
package main

import "fmt"

type ListNode struct {
	Val  int64
	Next *ListNode
}

func spiralMatrix(m, n int64, head *ListNode) [][]int64 {
	grid := make([][]int64, m)
	for i := range grid {
		grid[i] = make([]int64, n)
		for j := range grid[i] {
			grid[i][j] = -1
		}
	}
	moves := [4][2]int64{{0, 1}, {1, 0}, {0, -1}, {-1, 0}}
	var r, c, d int64
	for node := head; node != nil; node = node.Next {
		grid[r][c] = node.Val
		nr, nc := r+moves[d][0], c+moves[d][1]
		if nr < 0 || nr >= m || nc < 0 || nc >= n || grid[nr][nc] != -1 {
			d = (d + 1) % 4
		}
		r += moves[d][0]
		c += moves[d][1]
	}
	return grid
}

var seed int64 = 2326

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rows := [10]int64{100, 200, 250, 400, 500, 1000, 50, 125, 80, 160}
	heads := make([]*ListNode, 10)
	for k := 0; k < 10; k++ {
		var head *ListNode
		for i := 0; i < 90000+1111*k; i++ {
			head = &ListNode{Val: nextRandom() % 1001, Next: head}
		}
		heads[k] = head
	}
	var check int64
	for p := int64(0); p < 30; p++ {
		for k := int64(0); k < 10; k++ {
			m := rows[(p+k)%10]
			n := 100000 / m
			grid := spiralMatrix(m, n, heads[k])
			check = (check*31 + grid[p%m][(3*p+k)%n] + grid[m/2][n/2] + 2) % 1000000007
		}
	}
	fmt.Printf("30 passes over 10 lists in grids of 10^5 cells: checksum %d\n", check)
}
