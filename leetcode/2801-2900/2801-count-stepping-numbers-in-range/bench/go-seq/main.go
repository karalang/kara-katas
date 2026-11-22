// LeetCode #2801: Count Stepping Numbers in Range -- the bench in Go: the
// ★ arm over 400 ranges of 100-digit bounds made mostly of steps, all
// drawn first, then each answered 20 times.
package main

import "fmt"

const MOD = 1000000007

func walk(digits []int64, pos int, last int64, tight, started bool, memo [][10]int64) int64 {
	if pos == len(digits) {
		if started {
			return 1
		}
		return 0
	}
	free := started && !tight
	if free && memo[pos][last] >= 0 {
		return memo[pos][last]
	}
	top := int64(9)
	if tight {
		top = digits[pos]
	}
	var ways int64
	for d := int64(0); d <= top; d++ {
		nextTight := tight && d == top
		if !started {
			ways += walk(digits, pos+1, d, nextTight, d > 0, memo)
		} else if d-last == 1 || last-d == 1 {
			ways += walk(digits, pos+1, d, nextTight, true, memo)
		}
	}
	ways %= MOD
	if free {
		memo[pos][last] = ways
	}
	return ways
}

func countUpTo(s string) int64 {
	digits := make([]int64, len(s))
	for i := 0; i < len(s); i++ {
		digits[i] = int64(s[i]) - 48
	}
	memo := make([][10]int64, len(s))
	for i := range memo {
		for d := range memo[i] {
			memo[i][d] = -1
		}
	}
	return walk(digits, 0, 0, true, false, memo)
}

func steps(s string) bool {
	for i := 1; i < len(s); i++ {
		diff := int(s[i]) - int(s[i-1])
		if diff != 1 && diff != -1 {
			return false
		}
	}
	return true
}

func countSteppingNumbers(low, high string) int64 {
	var own int64
	if steps(low) {
		own = 1
	}
	return ((countUpTo(high)-countUpTo(low)+own)%MOD + MOD) % MOD
}

var seed int64 = 2801

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func number(m int) string {
	d := nextRandom()%9 + 1
	s := []byte{byte('0' + d)}
	for i := 1; i < m; i++ {
		r := nextRandom() % 10
		if r < 8 {
			if (r%2 == 0 && d > 0) || d == 9 {
				d--
			} else {
				d++
			}
		} else {
			d = r
		}
		s = append(s, byte('0'+d))
	}
	return string(s)
}

func main() {
	count := 400
	rounds := 20
	lows := make([]string, count)
	highs := make([]string, count)
	for c := 0; c < count; c++ {
		a := number(100)
		b := number(100)
		if a <= b {
			lows[c], highs[c] = a, b
		} else {
			lows[c], highs[c] = b, a
		}
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for c := 0; c < count; c++ {
			a := countSteppingNumbers(lows[c], highs[c])
			total += a
			check = (check*31 + a + r) % 1000000007
		}
	}
	fmt.Printf("%d ranges of 100 digits, %d rounds: counts sum to %d, checksum %d\n", count, rounds, total, check)
}
