// LeetCode 282 par-lane mirror — Go. One goroutine per input, over the same
// 220 independent searches.
package main

import (
	"fmt"
	"sync"
)

const Inputs = 220
const NDig = 9

func makeInput(idx int64) []byte {
	seed := (20260820 + idx*7919) % 2147483648
	v := make([]byte, NDig)
	for d := 0; d < NDig; d++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		v[d] = byte('0' + 1 + (seed/19)%6)
	}
	return v
}
func targetFor(idx int64) int64 {
	seed := (20260820 + idx*7919) % 2147483648
	for d := 0; d < 10; d++ {
		seed = (seed*1103515245 + 12345) % 2147483648
	}
	return (seed / 23) % 40
}
func search(num []byte, target int64, pos int, expr string, cur, last int64, found, hash *int64) {
	if pos == NDig {
		if cur == target {
			*found++
			*hash = (*hash*31 + int64(len(expr))) % 1000000007
		}
		return
	}
	for end := pos + 1; end <= NDig; end++ {
		if end > pos+1 && num[pos] == '0' {
			return
		}
		var n int64
		for k := pos; k < end; k++ {
			n = n*10 + int64(num[k]-'0')
		}
		piece := string(num[pos:end])
		if pos == 0 {
			search(num, target, end, piece, n, n, found, hash)
		} else {
			search(num, target, end, expr+"+"+piece, cur+n, n, found, hash)
			search(num, target, end, expr+"-"+piece, cur-n, -n, found, hash)
			search(num, target, end, expr+"*"+piece, cur-last+last*n, last*n, found, hash)
		}
	}
}
func solveOne(i int64) int64 {
	num := makeInput(i)
	target := targetFor(i)
	var found, hash int64
	search(num, target, 0, "", 0, 0, &found, &hash)
	return (i*1000003 + found*31 + hash) % 1000000007
}
func main() {
	parts := make([]int64, Inputs)
	var wg sync.WaitGroup
	for i := int64(0); i < Inputs; i++ {
		wg.Add(1)
		go func(i int64) {
			defer wg.Done()
			parts[i] = solveOne(i)
		}(i)
	}
	wg.Wait()
	var sink int64
	for _, v := range parts {
		sink = (sink + v) % 1000000007
	}
	fmt.Println(sink)
}
