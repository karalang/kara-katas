// LeetCode #119 — Go mirror, in-place single-row Pascal.
// Same algorithm + workload as get_row.kara: one []int64 of length rowIndex+1 (data-dependent
// rowIndex = 30 + acc%20), updated in place right-to-left, folding every entry. K=440000. GC data point.
package main

import "fmt"

const MOD int64 = 1000000007

func getRow(ri int64) []int64 {
	n := ri + 1
	row := make([]int64, n)
	for j := int64(0); j < n; j++ {
		row[j] = 1
	}
	for i := int64(2); i <= ri; i++ {
		for k := i - 1; k >= 1; k-- {
			row[k] = row[k] + row[k-1]
		}
	}
	return row
}

func rowHash(row []int64) int64 {
	var h int64 = 1
	for _, x := range row {
		h = (h*131 + x) % MOD
	}
	return (h*31 + int64(len(row)) + 7) % MOD
}

func main() {
	var acc int64 = 0
	for rep := 0; rep < 440000; rep++ {
		ri := 30 + (acc % 20)
		acc = (acc*131 + rowHash(getRow(ri))) % MOD
	}
	fmt.Println(acc)
}
