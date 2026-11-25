// LeetCode #1362 bench -- Go: d counts down from the square root of
// num + 2, and the first d that divides num + 1 or num + 2 gives the answer.
package main

import (
	"fmt"
	"math"
)

func isqrt(x int64) int64 {
	r := int64(math.Sqrt(float64(x)))
	for r*r > x {
		r--
	}
	for (r+1)*(r+1) <= x {
		r++
	}
	return r
}

func closestDivisors(num int32) []int32 {
	one, two := int64(num)+1, int64(num)+2
	for d := isqrt(two); d > 0; d-- {
		if one%d == 0 {
			return []int32{int32(d), int32(one / d)}
		}
		if two%d == 0 {
			return []int32{int32(d), int32(two / d)}
		}
	}
	return []int32{1, num + 1}
}

func main() {
	// 10^4 questions, each num up to 10^9 drawn from the checksum so far,
	// both parts of every answer folded into it
	var check int64
	for r := int64(0); r < 10000; r++ {
		num := int32(1 + (check*7919+r)%1000000000)
		pair := closestDivisors(num)
		check = (check*31 + int64(pair[0])*7 + int64(pair[1]) + r) % 1000000007
	}
	fmt.Printf("10000 questions: checksum %d\n", check)
}
