// LeetCode #2260: Minimum Consecutive Cards to Pick Up -- Go mirror of
// the ★ arm: a map of where each value was last seen, every repeat a
// candidate run. Same workload and checksum as cards.kara.
package main

import "fmt"

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func minimumCardPickup(cards []int64) int64 {
	last := map[int64]int64{}
	best := int64(-1)
	for i, card := range cards {
		if j, ok := last[card]; ok {
			run := int64(i) - j + 1
			if best < 0 || run < best {
				best = run
			}
		}
		last[card] = int64(i)
	}
	return best
}

func main() {
	seed := int64(2260)
	check := int64(0)
	tops := []int64{1000000, 100000, 10000}
	cards := make([]int64, 100000)
	for t := 0; t < 300; t++ {
		for i := range cards {
			hi := nextRandom(&seed)
			cards[i] = (hi*32768 + nextRandom(&seed)) % tops[t%3]
		}
		check = (check*31 + minimumCardPickup(cards) + 2) % 1000000007
	}
	fmt.Printf("300 hands of 10^5 cards: checksum %d\n", check)
}
