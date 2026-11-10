// LeetCode #2087: Minimum Cost Homecoming of a Robot in a Grid -- Go
// mirror of the ★ arm's benchmark (homecoming.kara): the same grid and
// 2000 trips, each the two ranges of costs summed over slices.
package main

import "fmt"

var seed int64 = 2087

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func sum(costs []int64) int64 {
	var s int64
	for _, c := range costs {
		s += c
	}
	return s
}

func walk(costs []int64, from, to int64) int64 {
	if from < to {
		return sum(costs[from+1 : to+1])
	}
	return sum(costs[to:from])
}

func minCost(start, home []int64, rows, cols []int64) int64 {
	return walk(rows, start[0], home[0]) + walk(cols, start[1], home[1])
}

func place() int64 {
	hi := nextRandom()
	return (hi*32768 + nextRandom()) % 1000000
}

func main() {
	rows := make([]int64, 1000000)
	for i := range rows {
		rows[i] = nextRandom() % 10001
	}
	cols := make([]int64, 1000000)
	for i := range cols {
		cols[i] = nextRandom() % 10001
	}
	var total, check int64
	for k := 0; k < 2000; k++ {
		r := place()
		start := []int64{r, place()}
		r = place()
		home := []int64{r, place()}
		a := minCost(start, home, rows, cols)
		total += a
		check = (check*31 + a) % 1000000007
	}
	fmt.Printf("2000 trips: sum %d, checksum %d\n", total, check)
}
