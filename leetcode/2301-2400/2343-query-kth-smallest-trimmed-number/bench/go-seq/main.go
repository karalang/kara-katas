// LeetCode #2343: Query Kth Smallest Trimmed Number -- the bench, the ★ arm
// in Go: for each query the indices sorted by their trimmed text, compared
// in place, and then by index, and the k-th taken.
package main

import (
	"fmt"
	"sort"
	"strings"
)

func smallestTrimmedNumbers(nums []string, queries [][2]int64) []int64 {
	width := len(nums[0])
	answer := make([]int64, 0, len(queries))
	for _, query := range queries {
		k, trim := query[0], int(query[1])
		order := make([]int, len(nums))
		for i := range order {
			order[i] = i
		}
		sort.Slice(order, func(x, y int) bool {
			a, b := order[x], order[y]
			c := strings.Compare(nums[a][width-trim:], nums[b][width-trim:])
			if c != 0 {
				return c < 0
			}
			return a < b
		})
		answer = append(answer, int64(order[k-1]))
	}
	return answer
}

func scrambled(index int64) int64 {
	return index * 2654435761 % 2147483647
}

func main() {
	type kase struct {
		nums    []string
		queries [][2]int64
	}
	cases := make([]kase, 0, 10)
	for c := int64(0); c < 10; c++ {
		nums := make([]string, 100)
		for i := int64(0); i < 100; i++ {
			var b strings.Builder
			for d := int64(0); d < 100; d++ {
				b.WriteByte(byte('0' + scrambled(c*10000+i*100+d)%10))
			}
			nums[i] = b.String()
		}
		queries := make([][2]int64, 100)
		for q := int64(0); q < 100; q++ {
			queries[q] = [2]int64{1 + scrambled(c*1000+q+500000)%100, 1 + scrambled(c*1000+q+700000)%100}
		}
		cases = append(cases, kase{nums, queries})
	}
	check := int64(0)
	for p := int64(0); p < 50; p++ {
		for _, cs := range cases {
			for _, i := range smallestTrimmedNumbers(cs.nums, cs.queries) {
				check = (check*31 + i + p) % 1000000007
			}
		}
	}
	fmt.Printf("50 passes over 10 cases of 100 numbers of 100 digits under 100 queries: checksum %d\n", check)
}
