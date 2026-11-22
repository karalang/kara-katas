// LeetCode #2818: Apply Operations to Maximize Score -- the bench's Go
// mirror of the ★ arm: a sieve of prime scores, one monotonic stack, the
// indices sorted by value, largest first, each power by squaring.
package main

import (
	"fmt"
	"slices"
)

const mod = 1000000007

func power(base, exp int64) int64 {
	result, b, e := int64(1), base%mod, exp
	for e > 0 {
		if e%2 == 1 {
			result = result * b % mod
		}
		b = b * b % mod
		e /= 2
	}
	return result
}

func maximumScore(nums []int64, k int64) int64 {
	n := len(nums)
	top := slices.Max(nums)
	score := make([]int64, top+1)
	for p := int64(2); p <= top; p++ {
		if score[p] == 0 {
			for q := p; q <= top; q += p {
				score[q]++
			}
		}
	}
	s := make([]int64, n)
	left := make([]int64, n)
	right := make([]int64, n)
	for i := range nums {
		s[i] = score[nums[i]]
		left[i] = -1
		right[i] = int64(n)
	}
	stack := []int{}
	for i := 0; i < n; i++ {
		for len(stack) > 0 && s[stack[len(stack)-1]] < s[i] {
			right[stack[len(stack)-1]] = int64(i)
			stack = stack[:len(stack)-1]
		}
		if len(stack) > 0 {
			left[i] = int64(stack[len(stack)-1])
		}
		stack = append(stack, i)
	}
	order := make([]int, n)
	for i := range order {
		order[i] = i
	}
	slices.SortFunc(order, func(a, b int) int {
		if nums[a] > nums[b] {
			return -1
		}
		if nums[a] < nums[b] {
			return 1
		}
		return 0
	})
	rest, total := k, int64(1)
	for _, i := range order {
		if rest == 0 {
			break
		}
		take := (int64(i) - left[i]) * (right[i] - int64(i))
		if take > rest {
			take = rest
		}
		total = total * power(nums[i], take) % mod
		rest -= take
	}
	return total
}

var seed int64 = 2818

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	count, rounds, n := 20, 3, 100000
	cases := make([][]int64, count)
	ks := make([]int64, count)
	for c := 0; c < count; c++ {
		cases[c] = make([]int64, n)
		for i := 0; i < n; i++ {
			cases[c][i] = wide()%100000 + 1
		}
		ks[c] = wide()%1000000000 + 1
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for c := 0; c < count; c++ {
			a := maximumScore(cases[c], ks[c])
			total += a
			check = (check*31 + a + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d, %d rounds: scores sum to %d, checksum %d\n", count, n, rounds, total, check)
}
