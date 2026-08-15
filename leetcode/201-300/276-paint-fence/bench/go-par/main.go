// LeetCode 276 par-lane mirror — goroutines. Same 16-branch split as
// paint_enum.kara, hand-parallelized the way a Go programmer would write it.
package main

import (
	"fmt"
	"sync"
)

const N = 13
const K = 4

func countPrefix(p0, p1 int64) int64 {
	var c [N]int64
	c[0] = p0
	c[1] = p1
	var count int64
	for {
		ok := true
		for i := 2; i < N; i++ {
			if c[i] == c[i-1] && c[i-1] == c[i-2] {
				ok = false
			}
		}
		if ok {
			count++
		}
		p := N - 1
		for p >= 2 && c[p] == K-1 {
			c[p] = 0
			p--
		}
		if p < 2 {
			break
		}
		c[p]++
	}
	return count
}

func main() {
	const prefixes = K * K
	parts := make([]int64, prefixes)
	var wg sync.WaitGroup
	for pre := 0; pre < prefixes; pre++ {
		wg.Add(1)
		go func(pre int) {
			defer wg.Done()
			parts[pre] = countPrefix(int64(pre)/K, int64(pre)%K)
		}(pre)
	}
	wg.Wait()
	var total int64
	for _, v := range parts {
		total += v
	}
	fmt.Println(total)
}
