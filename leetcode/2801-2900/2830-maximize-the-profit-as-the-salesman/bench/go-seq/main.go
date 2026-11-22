// LeetCode #2830: Maximize the Profit as the Salesman -- the bench's Go
// mirror of the ★ arm: the offers filed by their last house, and best[i]
// the most gold from the first i houses.
package main

import "fmt"

type sale struct{ start, gold int64 }

func maximizeTheProfit(n int64, offers [][3]int64) int64 {
	ending := make([][]sale, n)
	for _, o := range offers {
		ending[o[1]] = append(ending[o[1]], sale{o[0], o[2]})
	}
	best := make([]int64, n+1)
	for i := int64(0); i < n; i++ {
		best[i+1] = best[i]
		for _, s := range ending[i] {
			best[i+1] = max(best[i+1], best[s.start]+s.gold)
		}
	}
	return best[n]
}

var seed int64 = 2830

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	count, rounds, n := 20, 10, int64(100000)
	streets := make([][][3]int64, count)
	for c := range streets {
		streets[c] = make([][3]int64, n)
		for j := range streets[c] {
			start := wide() % n
			end := min(start+nextRandom()%100, n-1)
			streets[c][j] = [3]int64{start, end, nextRandom()%1000 + 1}
		}
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for _, offers := range streets {
			a := maximizeTheProfit(n, offers)
			total += a
			check = (check*31 + a + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d streets of %d, %d rounds: gold totals %d, checksum %d\n", count, n, rounds, total, check)
}
