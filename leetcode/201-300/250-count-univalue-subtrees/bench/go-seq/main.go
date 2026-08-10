// Benchmark workload for LeetCode #250 — Count Univalue Subtrees (Go mirror).
// Mirrors count_univalue.kara algorithm-for-algorithm.
package main

import "fmt"

func main() {
	var nodesN int64 = 2000000
	var passes int64 = 40
	var alphabet int64 = 3

	val := make([]int64, nodesN)
	var state int64 = 250250
	for i := int64(0); i < nodesN; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		val[i] = (state / 65536) % alphabet
	}

	uni := make([]bool, nodesN)

	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		var total int64 = 0
		for j := nodesN - 1; j >= 0; j-- {
			left := 2*j + 1
			right := 2*j + 2
			ok := true
			if left < nodesN {
				if !uni[left] || val[left] != val[j] {
					ok = false
				}
			}
			if right < nodesN {
				if !uni[right] || val[right] != val[j] {
					ok = false
				}
			}
			uni[j] = ok
			if ok {
				total++
			}
		}
		sink = (sink + total) % 1000000007
	}
	fmt.Println(sink)
}
