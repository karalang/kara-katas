// Benchmark twin for LeetCode #292 — same algorithm as nimgame.kara.
package main

import "fmt"

const n = 20000000

func main() {
	win := make([]bool, n+1)
	win[0] = false
	for i := 1; i <= n; i++ {
		w := false
		for take := 1; take <= 3; take++ {
			if i-take >= 0 && !win[i-take] {
				w = true
			}
		}
		win[i] = w
	}
	var losing, checksum int64
	for i := 0; i <= n; i++ {
		if !win[i] {
			losing++
			checksum = (checksum*31 + int64(i)) % 1000000007
		}
	}
	fmt.Printf("losing %d checksum %d\n", losing, checksum)
}
