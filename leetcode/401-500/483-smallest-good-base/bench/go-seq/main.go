// Benchmark for #483: Go mirror of the ★ arm (the most 1s first, a float
// root); see ../smallest_good_base.kara.
package main

import (
	"fmt"
	"math"
	"strconv"
)

func isOnes(n, k, m int64) bool {
	var sum, term int64 = 1, 1
	for i := int64(1); i < m; i++ {
		if term > (n-sum)/k {
			return false
		}
		term *= k
		sum += term
	}
	return sum == n
}

func smallestGoodBase(n string) string {
	value, _ := strconv.ParseInt(n, 10, 64)
	for m := int64(63); m >= 3; m-- {
		root := int64(math.Pow(float64(value), 1.0/float64(m-1)))
		for k := root; k < root+2; k++ {
			if k >= 2 && isOnes(value, k, m) {
				return strconv.FormatInt(k, 10)
			}
		}
	}
	return strconv.FormatInt(value-1, 10)
}

func main() {
	var count int64 = 50000
	var total, checksum int64
	for i := int64(0); i < count; i++ {
		n := int64(1000000000000000000) - 7*i
		if i%3 == 2 {
			k := 2 + i/3
			m := 3 + (i/3)%6
			n = 1
			var term int64 = 1
			for j := int64(1); j < m; j++ {
				if term > (1000000000000000000-n)/k {
					break
				}
				term *= k
				n += term
			}
		}
		base, _ := strconv.ParseInt(smallestGoodBase(strconv.FormatInt(n, 10)), 10, 64)
		total += base % 1000
		checksum = (checksum*31 + base%1000000007) % 1000000007
	}
	fmt.Printf("%d values: bases add up to %d (mod 1000 each), checksum %d\n", count, total, checksum)
}
