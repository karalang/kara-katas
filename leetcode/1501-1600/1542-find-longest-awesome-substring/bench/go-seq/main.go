// LeetCode #1542: Find Longest Awesome Substring -- bench: the ★ arm (prefix
// parity masks, first places in a slice) over 100 strings of 1 to 100000
// digits, each over its own first 1 to 10, built once, each asked 4 times.
// Go mirror of awesome.kara.
package main

import "fmt"

func longestAwesome(s string) int64 {
	n := int64(len(s))
	first := make([]int64, 1024)
	for m := range first {
		first[m] = n + 1
	}
	first[0] = 0
	mask, best := 0, int64(0)
	for i := 0; i < len(s); i++ {
		mask ^= 1 << (s[i] - '0')
		end := int64(i) + 1
		if end-first[mask] > best {
			best = end - first[mask]
		}
		for d := 0; d < 10; d++ {
			if l := end - first[mask^(1<<d)]; l > best {
				best = l
			}
		}
		if first[mask] > n {
			first[mask] = end
		}
	}
	return best
}

var seed int64 = 1542

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	strings := make([]string, 0, 100)
	for k := 0; k < 100; k++ {
		a := nextRandom()
		n := (a*32768+nextRandom())%100000 + 1
		digits := nextRandom()%10 + 1
		b := make([]byte, n)
		for i := range b {
			b[i] = byte('0' + nextRandom()%digits)
		}
		strings = append(strings, string(b))
	}
	check := int64(0)
	for p := 0; p < 4; p++ {
		for _, s := range strings {
			check = mix(check, longestAwesome(s))
		}
	}
	fmt.Printf("4 passes over 100 strings of up to 100000 digits: checksum %d\n", check)
}
