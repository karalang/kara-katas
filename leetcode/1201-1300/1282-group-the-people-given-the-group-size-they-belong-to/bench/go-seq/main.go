// LeetCode #1282 bench, in Go: the ★ arm (one open group per size, handed
// out when full) on 50 problems of 10000 people, built once, 500 rounds,
// every group folded into a checksum.
package main

import "fmt"

func groupThePeople(groupSizes []int64) [][]int64 {
	n := len(groupSizes)
	open := make([][]int64, 0)
	for i := 0; i <= n; i++ {
		open = append(open, []int64{})
	}
	groups := make([][]int64, 0)
	for person, size := range groupSizes {
		open[size] = append(open[size], int64(person))
		if int64(len(open[size])) == size {
			full := make([]int64, size)
			copy(full, open[size])
			groups = append(groups, full)
			open[size] = open[size][:0]
		}
	}
	return groups
}

var seed int64

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func problem(n int64) []int64 {
	sizes := make([]int64, 0, n)
	for int64(len(sizes)) < n {
		left := n - int64(len(sizes))
		var cap int64
		if nextRandom()%4 == 0 {
			cap = min(left, 1000)
		} else {
			cap = min(left, 8)
		}
		s := nextRandom()%cap + 1
		for k := int64(0); k < s; k++ {
			sizes = append(sizes, s)
		}
	}
	for i := n - 1; i > 0; i-- {
		j := nextRandom() % (i + 1)
		sizes[i], sizes[j] = sizes[j], sizes[i]
	}
	return sizes
}

func main() {
	seed = 1282
	problems := make([][]int64, 0)
	for k := 0; k < 50; k++ {
		problems = append(problems, problem(10000))
	}
	var check int64
	for round := int64(0); round < 500; round++ {
		for _, sizes := range problems {
			for _, g := range groupThePeople(sizes) {
				for _, p := range g {
					check = (check*131 + p + round) % 1000000007
				}
				check = (check*131 + 7) % 1000000007
			}
		}
	}
	fmt.Printf("500 rounds of 50 problems of 10000 people: checksum %d\n", check)
}
