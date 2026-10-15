// Benchmark for #655: each node placed from its parent, as the Kara ★ arm.
package main

import (
	"fmt"
	"strconv"
)

type TreeNode struct {
	val         int64
	left, right *TreeNode
}

func height(node *TreeNode) int64 {
	if node == nil {
		return 0
	}
	l, r := height(node.left), height(node.right)
	if l > r {
		return 1 + l
	}
	return 1 + r
}

func place(node *TreeNode, row, column, h int64, grid [][]string) {
	if node == nil {
		return
	}
	grid[row][column] = strconv.FormatInt(node.val, 10)
	if row < h {
		step := int64(1) << (h - row - 1)
		place(node.left, row+1, column-step, h, grid)
		place(node.right, row+1, column+step, h, grid)
	}
}

func printTree(root *TreeNode) [][]string {
	h := height(root) - 1
	columns := (int64(1) << (h + 1)) - 1
	grid := make([][]string, h+1)
	for r := range grid {
		grid[r] = make([]string, columns)
	}
	place(root, 0, (columns-1)/2, h, grid)
	return grid
}

var seed int64 = 655

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTree(levels, chance int64) *TreeNode {
	if levels == 0 {
		return nil
	}
	n := &TreeNode{val: nextRandom()%199 - 99}
	if nextRandom()%100 < chance {
		n.left = randomTree(levels-1, chance)
	}
	if nextRandom()%100 < chance {
		n.right = randomTree(levels-1, chance)
	}
	return n
}

func main() {
	inputs, rounds := 8, 10000
	trees := []*TreeNode{}
	for i := 0; i < inputs; i++ {
		trees = append(trees, randomTree(10, 85))
	}
	var cells, checksum int64
	for r := 0; r < rounds; r++ {
		grid := printTree(trees[(r*3)%inputs])
		var filled, chars int64
		for _, row := range grid {
			for _, cell := range row {
				if len(cell) > 0 {
					filled++
					chars += int64(len(cell))
				}
			}
		}
		cells += int64(len(grid) * len(grid[0]))
		checksum = (checksum*31 + filled*1000 + chars) % 1000000007
	}
	fmt.Printf("%d trees, %d rounds: %d cells, checksum %d\n", inputs, rounds, cells, checksum)
}
