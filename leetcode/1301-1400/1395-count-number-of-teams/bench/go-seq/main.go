// LeetCode #1395 bench, Go mirror of the ★ arm.
package main

import "fmt"

func numTeams(rating []int32) int32 {
	n := len(rating)
	var teams int32
	for j := 0; j < n; j++ {
		var lessLeft, greaterLeft, lessRight, greaterRight int32
		for i := 0; i < j; i++ {
			if rating[i] < rating[j] {
				lessLeft++
			} else {
				greaterLeft++
			}
		}
		for k := j + 1; k < n; k++ {
			if rating[k] < rating[j] {
				lessRight++
			} else {
				greaterRight++
			}
		}
		teams += lessLeft*greaterRight + greaterLeft*lessRight
	}
	return teams
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const n = 1000
	var seed int64 = 1395
	rating := make([]int32, n)
	for v := 1; v <= n; v++ {
		rating[v-1] = int32(v * 97)
	}
	for i := int64(n - 1); i >= 1; i-- {
		j := nextRandom(&seed) % (i + 1)
		rating[i], rating[j] = rating[j], rating[i]
	}
	var check int64
	for round := 0; round < 300; round++ {
		seed = (seed + check) % 2147483648
		a := nextRandom(&seed) % n
		b := nextRandom(&seed) % n
		rating[a], rating[b] = rating[b], rating[a]
		check = (check*131 + int64(numTeams(rating))) % 1000000007
	}
	fmt.Printf("300 rounds over 1000 soldiers: checksum %d\n", check)
}
