// LeetCode #1541: Minimum Insertions to Balance a Parentheses String --
// bench: the ★ arm (one pass keeping the ')' still wanted) over 100 strings
// of 1 to 100000 parentheses, built once, each asked 10 times. Go mirror of
// balance.kara.
package main

import "fmt"

func minInsertions(s string) int64 {
	inserted, need := int64(0), int64(0)
	for _, c := range s {
		if c == '(' {
			if need%2 == 1 {
				inserted++
				need--
			}
			need += 2
		} else {
			need--
			if need < 0 {
				inserted++
				need = 1
			}
		}
	}
	return inserted + need
}

var seed int64 = 1541

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
		chance := nextRandom() % 101
		b := make([]byte, n)
		for i := range b {
			if nextRandom()%100 < chance {
				b[i] = '('
			} else {
				b[i] = ')'
			}
		}
		strings = append(strings, string(b))
	}
	check := int64(0)
	for p := 0; p < 10; p++ {
		for _, s := range strings {
			check = mix(check, minInsertions(s))
		}
	}
	fmt.Printf("10 passes over 100 strings of up to 100000 parentheses: checksum %d\n", check)
}
