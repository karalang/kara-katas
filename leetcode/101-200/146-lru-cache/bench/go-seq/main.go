package main

import "fmt"

func main() {
	var cap, keyRange, ops int64 = 1024, 4096, 32000000

	pool := cap + 2
	nkey := make([]int64, pool)
	nval := make([]int64, pool)
	nprev := make([]int64, pool)
	nnext := make([]int64, pool)
	for i := int64(0); i < pool; i++ {
		nkey[i] = -1
		nprev[i] = -1
		nnext[i] = -1
	}
	nnext[0] = 1
	nprev[1] = 0

	m := make(map[int64]int64)
	var size, sink, state int64 = 0, 0, 12345

	for t := int64(0); t < ops; t++ {
		state = (state*1103515245 + 12345) & 2147483647
		h1 := state >> 16
		state = (state*1103515245 + 12345) & 2147483647
		h2 := state >> 16
		key := h2 % keyRange

		if h1%2 == 0 {
			idx, ok := m[key]
			var r int64 = -1
			if ok {
				pi := nprev[idx]
				ni := nnext[idx]
				nnext[pi] = ni
				nprev[ni] = pi
				first := nnext[0]
				nprev[idx] = 0
				nnext[idx] = first
				nprev[first] = idx
				nnext[0] = idx
				r = nval[idx]
			}
			sink += r + 1
		} else {
			state = (state*1103515245 + 12345) & 2147483647
			v := state >> 16
			existing, ok := m[key]
			if ok {
				nval[existing] = v
				pi := nprev[existing]
				ni := nnext[existing]
				nnext[pi] = ni
				nprev[ni] = pi
				first := nnext[0]
				nprev[existing] = 0
				nnext[existing] = first
				nprev[first] = existing
				nnext[0] = existing
			} else {
				var idx int64
				if size < cap {
					idx = 2 + size
					size++
				} else {
					lru := nprev[1]
					pl := nprev[lru]
					nl := nnext[lru]
					nnext[pl] = nl
					nprev[nl] = pl
					delete(m, nkey[lru])
					idx = lru
				}
				nkey[idx] = key
				nval[idx] = v
				m[key] = idx
				first := nnext[0]
				nprev[idx] = 0
				nnext[idx] = first
				nprev[first] = idx
				nnext[0] = idx
			}
		}
	}
	fmt.Println(sink)
}
