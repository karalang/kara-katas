// LeetCode #1234 bench: the ★ arm in Go, over the same 40 strings of 10^5
// letters and 20 passes as the Kāra bench.
package main

import "fmt"

func index(c byte) int {
	switch c {
	case 'Q':
		return 0
	case 'W':
		return 1
	case 'E':
		return 2
	}
	return 3
}

func fits(outside *[4]int64, k int64) bool {
	for _, c := range outside {
		if c > k {
			return false
		}
	}
	return true
}

func balancedString(s string) int64 {
	n := int64(len(s))
	k := n / 4
	var outside [4]int64
	for i := 0; i < len(s); i++ {
		outside[index(s[i])]++
	}
	if outside[0] == k && outside[1] == k && outside[2] == k && outside[3] == k {
		return 0
	}
	best := n
	left := 0
	for right := 0; right < len(s); right++ {
		outside[index(s[right])]--
		for left <= right && fits(&outside, k) {
			if int64(right-left+1) < best {
				best = int64(right - left + 1)
			}
			outside[index(s[left])]++
			left++
		}
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1234)
	strings := make([]string, 40)
	for t := 0; t < 40; t++ {
		lean := int64(t % 4)
		b := make([]byte, 100000)
		for i := range b {
			r := nextRandom(&seed) % (4 + lean)
			switch {
			case r >= 4 || r == 0:
				b[i] = 'Q'
			case r == 1:
				b[i] = 'W'
			case r == 2:
				b[i] = 'E'
			default:
				b[i] = 'R'
			}
		}
		strings[t] = string(b)
	}
	check := int64(0)
	for pass := 0; pass < 20; pass++ {
		for _, s := range strings {
			check = (check*131 + balancedString(s)) % 1000000007
		}
	}
	fmt.Printf("40 strings of 10^5 letters, 20 passes: checksum %d\n", check)
}
