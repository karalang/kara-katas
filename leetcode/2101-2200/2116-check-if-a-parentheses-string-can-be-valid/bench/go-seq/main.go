// LeetCode #2116: Check if a Parentheses String Can Be Valid -- the
// benchmark, the same algorithm as valid.kara: two greedy passes over the
// bytes.

package main

import "fmt"

func canBeValid(s, locked []byte) bool {
	n := len(s)
	if n%2 == 1 {
		return false
	}
	var open int64
	for i := 0; i < n; i++ {
		if s[i] == '(' || locked[i] == '0' {
			open++
		} else {
			open--
			if open < 0 {
				return false
			}
		}
	}
	var close int64
	for i := n - 1; i >= 0; i-- {
		if s[i] == ')' || locked[i] == '0' {
			close++
		} else {
			close--
			if close < 0 {
				return false
			}
		}
	}
	return true
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(2116)
	const n = int64(50000)
	strings := make([][]byte, 0, 64)
	locks := make([][]byte, 0, 64)
	for k := 0; k < 64; k++ {
		flip := int64(-1)
		if nextRandom(&seed)%2 == 0 {
			flip = nextRandom(&seed) % n
		}
		s := make([]byte, 0, n)
		locked := make([]byte, 0, n)
		open := int64(0)
		for i := int64(0); i < n; i++ {
			var up bool
			if open == 0 {
				up = true
			} else if open == n-i {
				up = false
			} else {
				up = nextRandom(&seed)%2 == 0
			}
			if up {
				open++
			} else {
				open--
			}
			if i == flip {
				up = !up
			}
			if up {
				s = append(s, '(')
			} else {
				s = append(s, ')')
			}
			unlocked := nextRandom(&seed)%4 == 0 && k%2 == 0
			if unlocked {
				locked = append(locked, '0')
			} else {
				locked = append(locked, '1')
			}
		}
		strings = append(strings, s)
		locks = append(locks, locked)
	}
	var valid, check int64
	for round := int64(0); round < 40; round++ {
		for a := 0; a < 64; a++ {
			strings[a] = append(strings[a], '(', ')')
			locks[a] = append(locks[a], '1', '1')
			got := canBeValid(strings[a], locks[a])
			if got {
				valid++
				check = (check*31 + round + int64(a)) % 1000000007
			} else {
				check = (check*31 + 1) % 1000000007
			}
		}
	}
	fmt.Printf("2560 solves: %d can be valid, checksum %d\n", valid, check)
}
