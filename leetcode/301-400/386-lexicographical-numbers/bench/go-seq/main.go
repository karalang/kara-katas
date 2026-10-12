// Benchmark for #386: mirror of lexical_order.kara (step to the next number).
package main

import "fmt"

func lexicalOrder(n int64) []int64 {
	var out []int64
	cur := int64(1)
	for i := int64(0); i < n; i++ {
		out = append(out, cur)
		if cur*10 <= n {
			cur *= 10
		} else {
			for cur%10 == 9 || cur+1 > n {
				cur /= 10
			}
			cur++
		}
	}
	return out
}

func main() {
	var checksum int64
	for q := int64(0); q < 6000; q++ {
		v := lexicalOrder(50000 - q%1000)
		var sum int64
		for k := range v {
			sum += v[k] * int64(k+1)
		}
		checksum = (checksum*31 + sum) % 1000000007
	}
	fmt.Printf("6000 lists, checksum %d\n", checksum)
}
