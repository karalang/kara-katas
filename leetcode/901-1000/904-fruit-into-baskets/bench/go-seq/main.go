// LeetCode #904: Fruit Into Baskets -- bench program, Go.
//
// The last two types and the last run, over one row of 1,000,000 trees
// built once, of 3 types in runs of 1 to 50 trees. Each round finds the
// most fruit, folds it into a checksum and changes one tree's type.
package main

import "fmt"

func totalFruit(fruits []int64) int64 {
	var last, before int64 = -1, -1
	var run, current, best int64
	for _, f := range fruits {
		if f == last || f == before {
			current++
		} else {
			current = run + 1
		}
		if f == last {
			run++
		} else {
			run = 1
			before = last
			last = f
		}
		if current > best {
			best = current
		}
	}
	return best
}

var seed int64 = 904

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var trees int64 = 1000000
	var rounds int64 = 240
	fruits := make([]int64, 0, trees)
	for int64(len(fruits)) < trees {
		f := nextRandom() % 3
		r := 1 + nextRandom()%50
		for k := int64(0); k < r; k++ {
			if int64(len(fruits)) < trees {
				fruits = append(fruits, f)
			}
		}
	}
	var check, total int64
	for round := int64(0); round < rounds; round++ {
		got := totalFruit(fruits)
		total += got
		check = (check*31 + got) % 1000000007
		fruits[round*7919%trees] = nextRandom() % 3
	}
	fmt.Printf("%d rounds over %d trees: answers summing to %d, checksum %d\n", rounds, trees, total, check)
}
