// LeetCode #2782: Number of Unique Categories -- the bench in Go: the ★
// arm over 1000 sets of 100 elements from up to 100 categories, all
// drawn first, then each answered 100 times through the judge's handler,
// whose questions are counted.
package main

import "fmt"

type CategoryHandler struct {
	categories []int64
	asked      int64
}

func (h *CategoryHandler) haveSameCategory(a, b int64) bool {
	h.asked++
	n := int64(len(h.categories))
	return a >= 0 && b >= 0 && a < n && b < n && h.categories[a] == h.categories[b]
}

func numberOfCategories(n int64, handler *CategoryHandler) int64 {
	representatives := []int64{}
	for i := int64(0); i < n; i++ {
		found := false
		for _, r := range representatives {
			if handler.haveSameCategory(r, i) {
				found = true
				break
			}
		}
		if !found {
			representatives = append(representatives, i)
		}
	}
	return int64(len(representatives))
}

var seed int64 = 2782

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count := 1000
	rounds := 100
	handlers := make([]CategoryHandler, count)
	for c := 0; c < count; c++ {
		k := nextRandom()%100 + 1
		handlers[c].categories = make([]int64, 100)
		for i := range handlers[c].categories {
			handlers[c].categories[i] = nextRandom() % k
		}
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for c := 0; c < count; c++ {
			a := numberOfCategories(100, &handlers[c])
			total += a
			check = (check*31 + a + r) % 1000000007
		}
	}
	var asked int64
	for c := 0; c < count; c++ {
		asked += handlers[c].asked
	}
	fmt.Printf("%d sets of 100, %d rounds: categories sum to %d after %d questions, checksum %d\n", count, rounds, total, asked, check)
}
