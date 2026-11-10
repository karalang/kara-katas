// LeetCode #2107: Number of Unique Flavors After Sharing K Candies -- the
// benchmark, the same algorithm as flavors.kara: a map of the kept
// flavors' counts, the shared window sliding right one candy at a time.
package main

import "fmt"

func shareCandies(candies []int64, k int) int64 {
	kept := make(map[int64]int64)
	for _, c := range candies {
		kept[c]++
	}
	for _, c := range candies[:k] {
		kept[c]--
	}
	var distinct int64
	for _, n := range kept {
		if n > 0 {
			distinct++
		}
	}
	best := distinct
	for i := k; i < len(candies); i++ {
		kept[candies[i]]--
		if kept[candies[i]] == 0 {
			distinct--
		}
		kept[candies[i-k]]++
		if kept[candies[i-k]] == 1 {
			distinct++
		}
		if distinct > best {
			best = distinct
		}
	}
	return best
}

var seed int64 = 2107

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rows := make([][]int64, 0, 20)
	for r := 0; r < 20; r++ {
		flavors := nextRandom()%5000 + 1
		candies := make([]int64, 100000)
		for i := range candies {
			candies[i] = nextRandom()%flavors + 1
		}
		rows = append(rows, candies)
	}
	var total, check int64
	for _, candies := range rows {
		for q := 0; q < 5; q++ {
			hi := nextRandom()
			k := (hi*32768 + nextRandom()) % 100001
			got := shareCandies(candies, int(k))
			total += got
			check = (check*31 + got) % 1000000007
		}
	}
	fmt.Printf("100 shares: %d flavors kept, checksum %d\n", total, check)
}
