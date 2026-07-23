package main

import "fmt"

func windowHasDup(base []int64, w, width int64) bool {
	seen := make(map[int64]struct{})
	for t := int64(0); t < width; t++ {
		x := base[w+t]
		if _, ok := seen[x]; ok {
			return true
		}
		seen[x] = struct{}{}
	}
	return false
}

func main() {
	var big, width, m int64 = 240000, 800, 2000000

	base := make([]int64, 0, big)
	var state int64 = 12345
	for i := int64(0); i < big; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		base = append(base, state%m)
	}

	windows := big - width
	var sink int64 = 0
	for w := int64(0); w < windows; w++ {
		if windowHasDup(base, w, width) {
			sink++
		}
	}
	fmt.Println(sink)
}
