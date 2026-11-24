// LeetCode #1304 bench in Go: the ★ arm (the pairs i and -i, and 0 when n
// is odd, appended to a fresh slice), the same 10^6 calls.
package main

import "fmt"

func sumZero(n int64) []int64 {
	var out []int64
	for i := int64(1); i <= n/2; i++ {
		out = append(out, i, -i)
	}
	if n%2 == 1 {
		out = append(out, 0)
	}
	return out
}

func main() {
	var check int64
	for call := int64(0); call < 1000000; call++ {
		n := 1 + check%1000
		got := sumZero(n)
		x := got[(check/1000)%n]
		check = (check*31 + x + 1000 + call) % 1000000007
	}
	fmt.Printf("1000000 calls: checksum %d\n", check)
}
