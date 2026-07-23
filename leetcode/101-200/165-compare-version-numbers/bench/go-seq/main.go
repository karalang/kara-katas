package main

import (
	"fmt"
	"strconv"
	"strings"
)

func revisions(v string) []int64 {
	n := len(v)
	revs := make([]int64, 0, 4)
	i := 0
	for i < n {
		var val int64 = 0
		for i < n && v[i] != '.' {
			val = val*10 + int64(v[i]-'0')
			i++
		}
		revs = append(revs, val)
		i++ // skip the '.'
	}
	return revs
}

func compareVersion(v1, v2 string) int64 {
	a := revisions(v1)
	b := revisions(v2)
	na := len(a)
	nb := len(b)
	m := na
	if nb > m {
		m = nb
	}
	for i := 0; i < m; i++ {
		var x, y int64
		if i < na {
			x = a[i]
		}
		if i < nb {
			y = b[i]
		}
		if x < y {
			return -1
		}
		if x > y {
			return 1
		}
	}
	return 0
}

func main() {
	var m, passes int64 = 4096, 10000000
	pool := make([]string, m)
	var state int64 = 12345
	for k := int64(0); k < m; k++ {
		state = (state*1103515245 + 12345) & 2147483647
		r := 1 + (state % 4)
		parts := make([]string, 0, 4)
		for t := int64(0); t < r; t++ {
			state = (state*1103515245 + 12345) & 2147483647
			rev := state % 1000
			parts = append(parts, strconv.FormatInt(rev, 10))
		}
		pool[k] = strings.Join(parts, ".")
	}
	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		state = (state*1103515245 + 12345) & 2147483647
		i := state % m
		state = (state*1103515245 + 12345) & 2147483647
		j := state % m
		sink += compareVersion(pool[i], pool[j]) + 1
	}
	fmt.Println(sink)
}
