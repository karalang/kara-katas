package main

import "fmt"

func scan(bases []int64, stamp []int64, cnt []int64, n int64, pass int64) int64 {
	var mask int64 = 1048575 // 2^20 - 1
	var hash int64 = 0
	var dups int64 = 0
	for i := int64(0); i < n; i++ {
		hash = ((hash << 2) | bases[i]) & mask
		if i >= 9 {
			key := hash
			if stamp[key] != pass {
				stamp[key] = pass
				cnt[key] = 0
			}
			c := cnt[key] + 1
			cnt[key] = c
			if c == 2 {
				dups++
			}
		}
	}
	return dups
}

func main() {
	var n int64 = 1000000
	var passes int64 = 30
	var tablesize int64 = 1048576 // 2^20

	bases := make([]int64, n)
	var state int64 = 12345
	for b := int64(0); b < n; b++ {
		state = (state*1103515245 + 12345) & 2147483647
		bases[b] = (state >> 16) % 4
	}

	stamp := make([]int64, tablesize)
	cnt := make([]int64, tablesize)
	for t := int64(0); t < tablesize; t++ {
		stamp[t] = -1
		cnt[t] = 0
	}

	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		state = (state*1103515245 + 12345) & 2147483647
		idx := state % n
		bases[idx] = (state >> 16) % 4
		sink += scan(bases, stamp, cnt, n, p)
	}
	fmt.Println(sink)
}
