// LeetCode #1207 bench, in Go: the ★ arm (each value's count in a map, and
// the counts put in a set, a map to struct{}) on 2000 arrays of 1000
// values drawn once, then 10 rounds over the arrays, how many answer true
// folded into a checksum.
package main

import "fmt"

var seed int64 = 1207

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func uniqueOccurrences(arr []int64) bool {
	counts := map[int64]int64{}
	for _, v := range arr {
		counts[v]++
	}
	distinct := map[int64]struct{}{}
	for _, c := range counts {
		distinct[c] = struct{}{}
	}
	return len(distinct) == len(counts)
}

func main() {
	arrays := make([][]int64, 0, 2000)
	for a := 0; a < 2000; a++ {
		k := nextRandom()%12 + 1
		values := make([]int64, k)
		for j := range values {
			values[j] = nextRandom()%2001 - 1000
		}
		total := k * (k + 1) / 2
		arr := make([]int64, 1000)
		for i := range arr {
			r := nextRandom() % total
			j := int64(0)
			for r > j {
				r -= j + 1
				j++
			}
			arr[i] = values[j]
		}
		arrays = append(arrays, arr)
	}
	var check int64
	for round := int64(0); round < 10; round++ {
		var yes int64
		for _, arr := range arrays {
			if uniqueOccurrences(arr) {
				yes++
			}
		}
		check = (check*131 + yes + round) % 1000000007
	}
	fmt.Printf("10 rounds over 2000 arrays of 1000 values: checksum %d\n", check)
}
