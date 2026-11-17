// LeetCode #1598: Crawler Log Folder
// -- the bench in Go, mirroring crawler.kara: only the depth matters,
// read by switching on each log, on 2000 logs of 5000 operations, all
// drawn first.
package main

import "fmt"

func minOperations(logs []string) int32 {
	var depth int32
	for _, log := range logs {
		switch log {
		case "../":
			depth = max(depth-1, 0)
		case "./":
		default:
			depth++
		}
	}
	return depth
}

var seed int64 = 1598

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	all := make([][]string, 2000)
	for g := range all {
		all[g] = make([]string, 5000)
		for i := range all[g] {
			r := nextRandom() % 8
			if r < 2 {
				all[g][i] = "../"
			} else if r < 4 {
				all[g][i] = "./"
			} else {
				all[g][i] = fmt.Sprintf("d%d/", r-3)
			}
		}
	}
	var check, total int64
	for _, logs := range all {
		answer := minOperations(logs)
		total += int64(answer)
		check = (check*31 + int64(answer) + 1) % 1000000007
	}
	fmt.Printf("2000 logs of 5000 operations: total %d, checksum %d\n", total, check)
}
