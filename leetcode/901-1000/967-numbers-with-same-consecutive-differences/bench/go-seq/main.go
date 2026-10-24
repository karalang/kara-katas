// Benchmark: LeetCode #967 Numbers With Same Consecutive Differences --
// the ★ arm, level by level, for every n from 2 to 9 and every k from 0
// to 9. Mirrors nums_same_consec_diff.kara, .c, .rs and .py.
package main

import "fmt"

func numsSameConsecDiff(n, k int64) []int64 {
	level := []int64{1, 2, 3, 4, 5, 6, 7, 8, 9}
	for i := int64(1); i < n; i++ {
		var next []int64
		for _, x := range level {
			last := x % 10
			if last+k <= 9 {
				next = append(next, x*10+last+k)
			}
			if k > 0 && last-k >= 0 {
				next = append(next, x*10+last-k)
			}
		}
		level = next
	}
	return level
}

func main() {
	rounds := 2000
	var found, check int64
	for r := 0; r < rounds; r++ {
		for n := int64(2); n < 10; n++ {
			for k := int64(0); k < 10; k++ {
				for _, x := range numsSameConsecDiff(n, k) {
					found++
					check = (check*31 + x) % 1000000007
				}
			}
		}
	}
	fmt.Printf("%d rounds over n from 2 to 9 and k from 0 to 9: %d numbers, checksum %d\n", rounds, found, check)
}
