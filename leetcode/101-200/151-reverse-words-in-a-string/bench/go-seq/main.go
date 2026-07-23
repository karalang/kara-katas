package main

import "fmt"

func main() {
	var len_, passes, modp, space int64 = 200000, 320, 1000000007, 32
	buf := make([]int64, len_)
	ws := make([]int64, len_)
	we := make([]int64, len_)
	var state int64 = 12345
	for i := int64(0); i < len_; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		if state%100 < 15 {
			buf[i] = space
		} else {
			buf[i] = 97 + state%26
		}
	}

	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		state = (state*1103515245 + 12345) & 2147483647
		idx := state % len_
		state = (state*1103515245 + 12345) & 2147483647
		if state%100 < 15 {
			buf[idx] = space
		} else {
			buf[idx] = 97 + state%26
		}

		var i, m int64 = 0, 0
		for i < len_ {
			for i < len_ && buf[i] == space {
				i++
			}
			if i >= len_ {
				break
			}
			start := i
			for i < len_ && buf[i] != space {
				i++
			}
			ws[m] = start
			we[m] = i
			m++
		}

		for k := m - 1; k >= 0; k-- {
			if k < m-1 {
				sink = (sink*131 + space) % modp
			}
			e := we[k]
			for j := ws[k]; j < e; j++ {
				sink = (sink*131 + buf[j]) % modp
			}
		}
	}
	fmt.Println(sink)
}
