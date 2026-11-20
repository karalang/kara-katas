// LeetCode #1744: Can You Eat Your Favorite Candy on Your Favorite Day?
// -- the bench (eat.kara in Go): prefix sums, then two comparisons a
// query.
package main

import "fmt"

func canEat(candiesCount []int32, queries [][]int32) []bool {
	before := []int64{0}
	for _, c := range candiesCount {
		before = append(before, before[len(before)-1]+int64(c))
	}
	answers := []bool{}
	for _, q := range queries {
		t, day, cap := q[0], int64(q[1]), int64(q[2])
		answers = append(answers, day+1 <= before[t+1] && (day+1)*cap > before[t])
	}
	return answers
}

var seed int64 = 1744

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	const count, rounds, n = 10, 30, 100000
	candies := make([][]int32, count)
	queries := make([][][]int32, count)
	for c := 0; c < count; c++ {
		candies[c] = make([]int32, n)
		var total int64
		for i := range candies[c] {
			candies[c][i] = int32(nextRandom()%20 + 1)
			total += int64(candies[c][i])
		}
		queries[c] = make([][]int32, n)
		for i := range queries[c] {
			t := wide() % n
			day := wide() % total
			cap := nextRandom()%30 + 1
			queries[c][i] = []int32{int32(t), int32(day), int32(cap)}
		}
	}
	var yes, check int64
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < count; c++ {
			answers := canEat(candies[c], queries[c])
			var here int64
			for i, a := range answers {
				if a {
					here++
					check = (check + int64(i)*7 + r) % 1000000007
				}
			}
			yes += here
		}
	}
	fmt.Printf("%d problems of %d types and %d queries, %d rounds: %d yes, checksum %d\n", count, n, n, rounds, yes, check)
}
