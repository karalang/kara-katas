// LeetCode #2827: Number of Beautiful Integers in the Range -- the
// bench's Go mirror of the ★ arm: a digit DP up to high less one up to
// low - 1, the free started states memoized in a flat slice.
package main

import (
	"fmt"
	"strconv"
)

func walk(digits []int64, pos int, diff, rem int64, tight, started bool, k int64, memo []int64) int64 {
	n := len(digits)
	if pos == n {
		if started && diff == 0 && rem == 0 {
			return 1
		}
		return 0
	}
	key := (int64(pos)*(2*int64(n)+1)+diff+int64(n))*k + rem
	if !tight && started && memo[key] >= 0 {
		return memo[key]
	}
	top := int64(9)
	if tight {
		top = digits[pos]
	}
	var total int64
	for d := int64(0); d <= top; d++ {
		now := started || d > 0
		nextDiff := int64(0)
		if now {
			nextDiff = diff - 1
			if d%2 == 0 {
				nextDiff = diff + 1
			}
		}
		total += walk(digits, pos+1, nextDiff, (rem*10+d)%k, tight && d == top, now, k, memo)
	}
	if !tight && started {
		memo[key] = total
	}
	return total
}

func countUpto(x, k int64) int64 {
	if x <= 0 {
		return 0
	}
	text := strconv.FormatInt(x, 10)
	digits := make([]int64, len(text))
	for i := range text {
		digits[i] = int64(text[i] - '0')
	}
	n := int64(len(digits))
	memo := make([]int64, n*(2*n+1)*k)
	for i := range memo {
		memo[i] = -1
	}
	return walk(digits, 0, 0, 0, true, false, k, memo)
}

var seed int64 = 2827

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	count, rounds := 2000, 5
	lows := make([]int64, count)
	highs := make([]int64, count)
	ks := make([]int64, count)
	for c := 0; c < count; c++ {
		a, b := wide()%1000000000+1, wide()%1000000000+1
		lows[c], highs[c] = min(a, b), max(a, b)
		ks[c] = nextRandom()%20 + 1
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for c := 0; c < count; c++ {
			a := countUpto(highs[c], ks[c]) - countUpto(lows[c]-1, ks[c])
			total += a
			check = (check*31 + a + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d ranges, %d rounds: %d beautiful, checksum %d\n", count, rounds, total, check)
}
