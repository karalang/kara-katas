// LeetCode #118 — Go mirror ([][]int64), additive Pascal's triangle.
// Same algorithm + workload as generate.kara: each rep builds a full triangle of a data-dependent
// row count (30 + acc%16) as a nested [][]int64, folding every entry. K = 80000. The GC data point.
package main

import "fmt"

const MOD int64 = 1000000007

func generate(numRows int64) [][]int64 {
	tri := make([][]int64, 0, numRows)
	for i := int64(0); i < numRows; i++ {
		row := make([]int64, 0, i+1)
		for j := int64(0); j <= i; j++ {
			if j == 0 || j == i {
				row = append(row, 1)
			} else {
				row = append(row, tri[i-1][j-1]+tri[i-1][j])
			}
		}
		tri = append(tri, row)
	}
	return tri
}

func triangleHash(tri [][]int64) int64 {
	var h int64 = 1
	for _, row := range tri {
		for _, x := range row {
			h = (h*131 + x) % MOD
		}
		h = (h*31 + int64(len(row)) + 7) % MOD
	}
	return h
}

func main() {
	var acc int64 = 0
	for rep := 0; rep < 80000; rep++ {
		rows := 30 + (acc % 16)
		tri := generate(rows)
		h := triangleHash(tri)
		acc = (acc*131 + h) % MOD
	}
	fmt.Println(acc)
}
