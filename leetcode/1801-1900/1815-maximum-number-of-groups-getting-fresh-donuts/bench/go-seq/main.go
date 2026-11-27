// LeetCode #1815: Maximum Number of Groups Getting Fresh Donuts -- the
// bench in Go: the ★ arm over 3000 cases of 30 groups at a batch of 7 to
// 9, each group's remainder drawn from the batch's lower half, so that no
// two groups pair off and the search meets the most states.
package main

import "fmt"

func best(b int64, count []int64, left int64, memo map[int64]int64) int64 {
	var key int64
	for r := b - 1; r >= 1; r-- {
		key = key*31 + count[r]
	}
	if known, ok := memo[key]; ok {
		return known
	}
	var top int64
	any := false
	for r := int64(1); r < b; r++ {
		if count[r] > 0 {
			any = true
			count[r]--
			if got := best(b, count, (left+r)%b, memo); got > top {
				top = got
			}
			count[r]++
		}
	}
	if any && left == 0 {
		top++
	}
	memo[key] = top
	return top
}

func maxHappyGroups(batchSize int64, groups []int64) int64 {
	b := batchSize
	count := make([]int64, b)
	for _, g := range groups {
		count[g%b]++
	}
	happy := count[0]
	count[0] = 0
	for r := int64(1); r < b; r++ {
		s := b - r
		if r < s {
			k := count[r]
			if count[s] < k {
				k = count[s]
			}
			happy += k
			count[r] -= k
			count[s] -= k
		} else if r == s {
			happy += count[r] / 2
			count[r] %= 2
		}
	}
	return happy + best(b, count, 0, map[int64]int64{})
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1815)
	var check int64
	for c := 0; c < 3000; c++ {
		b := 7 + nextRandom(&seed)%3
		groups := make([]int64, 0, 30)
		for k := 0; k < 30; k++ {
			whole := nextRandom(&seed) * b
			groups = append(groups, whole+1+nextRandom(&seed)%((b-1)/2))
		}
		check = (check*31 + maxHappyGroups(b, groups)) % 1000000007
	}
	fmt.Printf("3000 cases: checksum %d\n", check)
}
