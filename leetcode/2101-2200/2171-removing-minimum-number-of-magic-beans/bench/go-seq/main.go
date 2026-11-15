// LeetCode #2171: Removing Minimum Number of Magic Beans -- the
// benchmark's Go mirror of beans.kara.
package main

import (
	"fmt"
	"sort"
)

func minimumRemoval(beans []int64) int64 {
	sorted := make([]int64, len(beans))
	copy(sorted, beans)
	sort.Slice(sorted, func(i, j int) bool { return sorted[i] < sorted[j] })
	n := int64(len(sorted))
	var total, kept int64
	for i := range sorted {
		total += sorted[i]
		if k := sorted[i] * (n - int64(i)); k > kept {
			kept = k
		}
	}
	return total - kept
}

var seed int64 = 2171

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	row := make([]int64, 0, 400000)
	for i := 0; i < 400000; i++ {
		a := nextRandom()
		b := nextRandom()
		row = append(row, (a*32768+b)%100000+1)
	}
	var check int64
	for r := 0; r < 100; r++ {
		a := nextRandom()
		b := nextRandom()
		start := (a*32768 + b) % 300001
		removed := minimumRemoval(row[start : start+100000])
		check = (check*31 + removed%1000000007) % 1000000007
	}
	fmt.Printf("100 solves: checksum %d\n", check)
}
