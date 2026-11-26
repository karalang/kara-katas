// LeetCode #1416 bench, Go: ways[i] counts the arrays the digits from i on
// can be read as, workload and checksum as number_of_arrays.kara.
package main

import (
	"fmt"
	"strings"
)

func numberOfArrays(s string, k int32) int32 {
	const modulus int64 = 1000000007
	n := len(s)
	ways := make([]int64, n+1)
	ways[n] = 1
	for i := n - 1; i >= 0; i-- {
		if s[i] == '0' {
			continue
		}
		var number int64
		for j := i; j < n; j++ {
			number = number*10 + int64(s[j]-'0')
			if number > int64(k) {
				break
			}
			ways[i] = (ways[i] + ways[j+1]) % modulus
		}
	}
	return int32(ways[0])
}

func main() {
	var seed int64 = 1416
	var pool strings.Builder
	lastZero := true
	for i := 0; i < 200000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		r := seed / 65536
		zero := !lastZero && r%10 == 0
		d := int64(0)
		if !zero {
			d = 1 + r%9
		}
		pool.WriteString(fmt.Sprintf("%d", d))
		lastZero = zero
	}
	p := pool.String()
	var check int64
	for w := 0; w < 100; w++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		start := seed / 65536 % 100000
		for p[start] == '0' {
			start++
		}
		seed = (seed*1103515245 + 12345) % 2147483648
		k := 1 + seed%1000000000
		check = (check*131 + int64(numberOfArrays(p[start:start+100000], int32(k)))) % 1000000007
	}
	fmt.Printf("100 windows of 10^5 digits: checksum %d\n", check)
}
