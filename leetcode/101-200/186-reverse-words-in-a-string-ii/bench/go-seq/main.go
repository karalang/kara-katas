package main

import "fmt"

func reverseRange(a []int64, lo, hi int64) {
	i, j := lo, hi
	for i < j {
		a[i], a[j] = a[j], a[i]
		i++
		j--
	}
}

func reverseWords(a []int64, n int64) {
	if n > 0 {
		reverseRange(a, 0, n-1)
	}
	var start int64 = 0
	for i := int64(0); i <= n; i++ {
		if i == n || a[i] == 32 {
			if i > start {
				reverseRange(a, start, i-1)
			}
			start = i + 1
		}
	}
}

func main() {
	var targetLen, passes int64 = 30000, 3000

	buf := make([]int64, 0, targetLen+16)
	var state int64 = 12345
	first := true
	for int64(len(buf)) < targetLen {
		if first {
			first = false
		} else {
			buf = append(buf, 32)
		}
		state = (state*1103515245 + 12345) & 2147483647
		wlen := 1 + (state % 8)
		for w := int64(0); w < wlen; w++ {
			state = (state*1103515245 + 12345) & 2147483647
			buf = append(buf, 97+(state%26))
		}
	}

	n := int64(len(buf))
	var modv int64 = 1000000007
	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		idx := (p*131 + 7) % n
		if buf[idx] != 32 {
			buf[idx] = 97 + (((buf[idx] - 97) + 1) % 26)
		}
		reverseWords(buf, n)
		var cs int64 = 0
		for k := int64(0); k < n; k++ {
			cs = (cs*131 + buf[k]) % modv
		}
		sink += cs
	}
	fmt.Println(sink)
}
