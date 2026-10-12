// LeetCode #420: Strong Password Checker -- Go mirror of
// strong_password.kara (count the runs by length mod 3).
package main

import "fmt"

func max64(a, b int64) int64 {
	if a > b {
		return a
	}
	return b
}

func min64(a, b int64) int64 {
	if a < b {
		return a
	}
	return b
}

func strongPasswordChecker(p string) int64 {
	n := int64(len(p))
	var lower, upper, digit int64
	for k := 0; k < len(p); k++ {
		b := p[k]
		if b >= 'a' && b <= 'z' {
			lower = 1
		} else if b >= 'A' && b <= 'Z' {
			upper = 1
		} else if b >= '0' && b <= '9' {
			digit = 1
		}
	}
	missing := 3 - lower - upper - digit
	var replace, zeroMod, oneMod int64
	var i int64
	for i < n {
		j := i
		for j < n && p[j] == p[i] {
			j++
		}
		run := j - i
		if run >= 3 {
			replace += run / 3
			if run%3 == 0 {
				zeroMod++
			} else if run%3 == 1 {
				oneMod++
			}
		}
		i = j
	}
	if n < 6 {
		return max64(missing, 6-n)
	}
	if n <= 20 {
		return max64(missing, replace)
	}
	del := n - 20
	left := del
	first := min64(left, zeroMod)
	replace -= first
	left -= first
	second := min64(left, 2*oneMod)
	replace -= second / 2
	left -= second
	replace -= min64(left/3, replace)
	return del + max64(missing, replace)
}

var seed int64 = 420

func step() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	calls := 10000000
	pool := "aAbB1."
	buf := make([]byte, 0, 1000008)
	for len(buf) < 1000000 {
		pick := pool[step()%6]
		run := 1 + step()%6
		for k := int64(0); k < run; k++ {
			buf = append(buf, pick)
		}
	}
	text := string(buf)
	var total, checksum int64
	for c := 0; c < calls; c++ {
		length := 1 + step()%50
		start := step() * 30 % (1000000 - length)
		answer := strongPasswordChecker(text[start : start+length])
		total += answer
		checksum = (checksum*31 + answer) % 1000000007
	}
	fmt.Printf("%d calls: total %d, checksum %d\n", calls, total, checksum)
}
