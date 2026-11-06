// LeetCode #1056: Confusing Number -- the benchmark, mirror of confusing.kara.
package main

import "fmt"

var turned = [10]int64{0, 1, -1, -1, -1, -1, 9, -1, 8, 6}

func confusingNumber(n int64) bool {
	rest := n
	upside := int64(0)
	for rest > 0 {
		d := turned[rest%10]
		if d < 0 {
			return false
		}
		upside = upside*10 + d
		rest /= 10
	}
	return upside != n
}

var seed int64 = 1056

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count = 500000
	const rounds = 20
	turning := [5]int64{0, 1, 6, 8, 9}
	other := [5]int64{2, 3, 4, 5, 7}
	numbers := make([]int64, 0)
	for i := 0; i < count; i++ {
		digits := 6 + nextRandom()%5
		spoiled := int64(-1)
		if nextRandom()%8 == 0 {
			spoiled = nextRandom() % digits
		}
		n := turning[1+nextRandom()%4]
		for k := int64(1); k < digits; k++ {
			var d int64
			if k == spoiled {
				d = other[nextRandom()%5]
			} else {
				d = turning[nextRandom()%5]
			}
			n = n*10 + d
		}
		numbers = append(numbers, n)
	}
	total := int64(0)
	check := int64(0)
	for r := 0; r < rounds; r++ {
		found := int64(0)
		for _, n := range numbers {
			if confusingNumber(n) {
				found++
				check = (check + n%1000) % 1000000007
			}
		}
		total += found
		check = (check*131 + found) % 1000000007
	}
	fmt.Printf("%d numbers, %d rounds: %d confusing, checksum %d\n", count, rounds, total, check)
}
