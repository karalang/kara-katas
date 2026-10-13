// Benchmark for #537: the ★ arm (split, then the schoolbook product);
// see ../../README.md § Benchmarks. Mirrors complex_number_multiply.kara.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

func parts(num string) (int64, int64) {
	halves := strings.Split(num, "+")
	re, _ := strconv.ParseInt(halves[0], 10, 64)
	im, _ := strconv.ParseInt(halves[1][:len(halves[1])-1], 10, 64)
	return re, im
}

func complexNumberMultiply(num1, num2 string) string {
	a, b := parts(num1)
	c, d := parts(num2)
	return fmt.Sprintf("%d+%di", a*c-b*d, a*d+b*c)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(537)
	nums := []string{}
	for k := 0; k < 2000; k++ {
		re := nextRandom(&seed)%201 - 100
		im := nextRandom(&seed)%201 - 100
		nums = append(nums, fmt.Sprintf("%d+%di", re, im))
	}
	n := len(nums)
	rounds := 2500
	real, length := 0, 0
	for r := 0; r < rounds; r++ {
		for i := 0; i < n; i++ {
			p := complexNumberMultiply(nums[i], nums[(i*7+r)%n])
			if strings.HasSuffix(p, "+0i") {
				real++
			}
			length += len(p)
		}
	}
	fmt.Printf("%d numbers, %d rounds: %d real, length %d\n", n, rounds, real, length)
}
