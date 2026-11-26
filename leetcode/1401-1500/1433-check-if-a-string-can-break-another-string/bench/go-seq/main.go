package main

import (
	"fmt"
	"slices"
)

func checkIfCanBreak(s1, s2 string) bool {
	a := []byte(s1)
	b := []byte(s2)
	slices.Sort(a)
	slices.Sort(b)
	up, down := true, true
	for i := range a {
		up = up && a[i] >= b[i]
		down = down && a[i] <= b[i]
	}
	return up || down
}

func main() {
	var seed int64 = 1433
	pool := make([]byte, 0, 1000000)
	up := make([]byte, 0, 1000000)
	for i := 0; i < 1000000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		c := byte('a' + seed/65536%25)
		seed = (seed*1103515245 + 12345) % 2147483648
		pool = append(pool, c)
		up = append(up, c+byte(seed/65536%2))
	}
	ps, us := string(pool), string(up)
	var breaks int64
	for i := 0; i < 400; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		high := seed / 65536
		seed = (seed*1103515245 + 12345) % 2147483648
		one := (high*32768 + seed/65536) % 900001
		seed = (seed*1103515245 + 12345) % 2147483648
		var got bool
		if seed/65536%2 == 0 {
			got = checkIfCanBreak(ps[one:one+100000], us[one:one+100000])
		} else {
			seed = (seed*1103515245 + 12345) % 2147483648
			high = seed / 65536
			seed = (seed*1103515245 + 12345) % 2147483648
			two := (high*32768 + seed/65536) % 900001
			got = checkIfCanBreak(ps[one:one+100000], ps[two:two+100000])
		}
		if got {
			breaks++
		}
	}
	fmt.Printf("400 pairs of 10^5 letters: %d can break\n", breaks)
}
