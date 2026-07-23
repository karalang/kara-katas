package main

import "fmt"

func prefixLPS(base []int64, w, width int64, comb, fail []int64) int64 {
	m := 2*width + 1
	for i := int64(0); i < width; i++ {
		comb[i] = base[w+i]
	}
	comb[width] = -1
	for i := int64(0); i < width; i++ {
		comb[width+1+i] = base[w+width-1-i]
	}

	fail[0] = 0
	var length int64 = 0
	var idx int64 = 1
	for idx < m {
		if comb[idx] == comb[length] {
			length++
			fail[idx] = length
			idx++
		} else if length > 0 {
			length = fail[length-1]
		} else {
			fail[idx] = 0
			idx++
		}
	}
	return fail[m-1]
}

func main() {
	var big, width, alpha int64 = 260000, 512, 2

	base := make([]int64, 0, big)
	var state int64 = 12345
	for i := int64(0); i < big; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		base = append(base, state%alpha)
	}

	m := 2*width + 1
	comb := make([]int64, m)
	fail := make([]int64, m)

	windows := big - width
	var sink int64 = 0
	for w := int64(0); w < windows; w++ {
		sink += prefixLPS(base, w, width, comb, fail)
	}
	fmt.Println(sink)
}
