// LeetCode #1411 bench, Go: rows of two colours and of three, 6 of each in
// the first row, workload and checksum as num_of_ways.kara.
package main

import "fmt"

func numOfWays(n int32) int32 {
	const modulus int64 = 1000000007
	var two, three int64 = 6, 6
	for i := int32(1); i < n; i++ {
		nextTwo := (3*two + 2*three) % modulus
		nextThree := (2*two + 2*three) % modulus
		two = nextTwo
		three = nextThree
	}
	return int32((two + three) % modulus)
}

func main() {
	var check int64
	for k := int64(0); k < 40000; k++ {
		n := 1 + (check+k)%5000
		check = (check*131 + int64(numOfWays(int32(n)))) % 1000000007
	}
	fmt.Printf("40000 grids of up to 5000 rows: checksum %d\n", check)
}
