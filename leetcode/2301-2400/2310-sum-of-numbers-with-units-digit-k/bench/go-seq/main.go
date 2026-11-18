// LeetCode #2310: Sum of Numbers With Units Digit K -- the bench, the ★
// arm in Go. The least count from 1 to 10 whose multiple of k fits within
// num and leaves a multiple of 10.
package main

import "fmt"

func minimumNumbers(num, k int64) int64 {
	if num == 0 {
		return 0
	}
	for n := int64(1); n <= 10; n++ {
		if n*k <= num && (num-n*k)%10 == 0 {
			return n
		}
	}
	return -1
}

func main() {
	var check int64
	for p := int64(0); p < 300; p++ {
		for num := int64(0); num <= 3000; num++ {
			for k := int64(0); k < 10; k++ {
				check = (check*31 + minimumNumbers(num, k) + 1 + p) % 1000000007
			}
		}
	}
	fmt.Printf("300 passes over 3001 sums and 10 digits: checksum %d\n", check)
}
