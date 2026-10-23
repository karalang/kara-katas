// LeetCode #881 bench: Go mirror of num_rescue_boats.kara (the ★ arm, sort,
// then two pointers) on the same 600 cases.
package main

import (
	"fmt"
	"slices"
)

func numRescueBoats(people []int64, limit int64) int64 {
	weights := slices.Clone(people)
	slices.Sort(weights)
	light, heavy := 0, len(weights)-1
	var boats int64
	for light <= heavy {
		if weights[light]+weights[heavy] <= limit {
			light++
		}
		heavy--
		boats++
	}
	return boats
}

var seed int64 = 881

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var total, check int64
	for k := 0; k < 600; k++ {
		n := 40000 + nextRandom()%10001
		x := nextRandom()
		y := nextRandom()
		limit := 1 + (x*32768+y)%30000
		people := make([]int64, 0, n)
		for i := int64(0); i < n; i++ {
			a := nextRandom()
			b := nextRandom()
			people = append(people, (a*32768+b)%limit+1)
		}
		boats := numRescueBoats(people, limit)
		total += boats
		check = (check*131 + boats) % 1000000007
	}
	fmt.Printf("600 cases of up to 50000 people: %d boats, checksum %d\n", total, check)
}
