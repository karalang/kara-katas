// LeetCode #859: Buddy Strings -- Go mirror of the bench program (the ★ arm,
// one pass over the positions where the strings differ).
package main

import "fmt"

func buddyStrings(a, b []byte) bool {
	if len(a) != len(b) {
		return false
	}
	first, second := -1, -1
	for i := 0; i < len(a); i++ {
		if a[i] != b[i] {
			if first < 0 {
				first = i
			} else if second < 0 {
				second = i
			} else {
				return false
			}
		}
	}
	if first < 0 {
		var seen [26]bool
		for _, c := range a {
			k := c - 97
			if seen[k] {
				return true
			}
			seen[k] = true
		}
		return false
	}
	return second >= 0 && a[first] == b[second] && a[second] == b[first]
}

var seed int64 = 859

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 20000
	s := make([]byte, n)
	for i := range s {
		s[i] = byte(97 + nextRandom()%26)
	}
	goal := make([]byte, n)
	copy(goal, s)
	var buddies, check int64
	for r := int64(0); r < 40000; r++ {
		i := nextRandom() % n
		j := nextRandom() % n
		kind := r % 3
		old := goal[i]
		if kind == 1 {
			goal[i] = byte(97 + (int64(old)-97+1+nextRandom()%25)%26)
		} else {
			goal[i], goal[j] = goal[j], goal[i]
		}
		k := nextRandom() % n
		l := nextRandom() % n
		if kind == 2 {
			goal[k], goal[l] = goal[l], goal[k]
		}
		yes := buddyStrings(s, goal)
		if kind == 2 {
			goal[k], goal[l] = goal[l], goal[k]
		}
		if kind == 1 {
			goal[i] = old
		} else {
			goal[i], goal[j] = goal[j], goal[i]
		}
		if yes {
			buddies++
		}
		v := int64(1)
		if yes {
			v = r + 2
		}
		check = (check*31 + v) % 1000000007
	}
	fmt.Printf("40000 rounds on 20000 letters: %d buddies, checksum %d\n", buddies, check)
}
