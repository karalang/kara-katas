// LeetCode #1714: Sum Of Special Evenly-Spaced Elements In Array -- the Go
// mirror of the bench (special.kara): the queries taken in order of their
// step, a small step's sums built from the back and a large step's walked,
// on 5 random problems of 50000 values and 150000 queries, each answered 4
// times.
package main

import (
	"fmt"
	"math"
	"sort"
)

// the floor of the square root, an f64 estimate stepped to the root
func isqrt(n int) int {
	r := int(math.Sqrt(float64(n)))
	for r*r > n {
		r--
	}
	for (r+1)*(r+1) <= n {
		r++
	}
	return r
}

func solve(nums []int32, queries [][]int32) []int32 {
	const modulus = 1000000007
	n := len(nums)
	small := isqrt(n)
	answer := make([]int32, len(queries))
	order := make([]int, len(queries))
	for i := range order {
		order[i] = i
	}
	sort.SliceStable(order, func(a, b int) bool { return queries[order[a]][1] < queries[order[b]][1] })
	sums := make([]int64, n)
	built := 0
	for _, q := range order {
		x, y := int(queries[q][0]), int(queries[q][1])
		if y <= small {
			if y != built {
				for j := n - 1; j >= 0; j-- {
					var after int64
					if j+y < n {
						after = sums[j+y]
					}
					sums[j] = (int64(nums[j]) + after) % modulus
				}
				built = y
			}
			answer[q] = int32(sums[x])
		} else {
			var total int64
			for j := x; j < n; j += y {
				total += int64(nums[j])
			}
			answer[q] = int32(total % modulus)
		}
	}
	return answer
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	a := nextRandom(seed)
	return a*32768 + nextRandom(seed)
}

func main() {
	count := 5
	var rounds int64 = 4
	var n int64 = 50000
	q := 150000
	var seed int64 = 1714
	numsAll := make([][]int32, count)
	queriesAll := make([][][]int32, count)
	for p := 0; p < count; p++ {
		nums := make([]int32, n)
		for i := range nums {
			nums[i] = int32(wide(&seed) % 1000000000)
		}
		queries := make([][]int32, q)
		for i := range queries {
			x := wide(&seed) % n
			var y int64
			if nextRandom(&seed)%2 == 0 {
				y = nextRandom(&seed)%223 + 1
			} else {
				y = wide(&seed)%n + 1
			}
			queries[i] = []int32{int32(x), int32(y)}
		}
		numsAll[p] = nums
		queriesAll[p] = queries
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for p := 0; p < count; p++ {
			for _, a := range solve(numsAll[p], queriesAll[p]) {
				sum += int64(a)
				check = (check*31 + int64(a) + r) % 1000000007
			}
		}
	}
	fmt.Printf("%d problems of %d values and %d queries, %d rounds: answers sum to %d, checksum %d\n", count, n, q, rounds, sum, check)
}
