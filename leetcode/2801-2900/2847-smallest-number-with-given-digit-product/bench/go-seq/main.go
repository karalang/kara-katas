// LeetCode #2847: Smallest Number With Given Digit Product -- the
// bench, mirrored from product.kara: the largest digit that divides
// what is left, 9 down to 2, and the digits smallest first.
package main

import "fmt"

func smallestNumber(n int64) string {
	if n == 1 {
		return "1"
	}
	rest := n
	digits := []byte{}
	for d := int64(9); d >= 2; d-- {
		for rest%d == 0 {
			digits = append(digits, byte('0'+d))
			rest /= d
		}
	}
	if rest != 1 {
		return "-1"
	}
	out := make([]byte, len(digits))
	for i := range digits {
		out[i] = digits[len(digits)-1-i]
	}
	return string(out)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds = 100000, 20
	seed := int64(2847)
	primes := [4]int64{2, 3, 5, 7}
	numbers := make([]int64, 0, count)
	for c := 0; c < count; c++ {
		n := int64(1)
		factors := nextRandom(&seed) % 41
		for i := int64(0); i < factors; i++ {
			p := primes[nextRandom(&seed)%4]
			if n <= 1000000000000000000/p {
				n *= p
			}
		}
		if nextRandom(&seed)%10 == 0 && n <= 1000000000000000000/11 {
			n *= 11
		}
		numbers = append(numbers, n)
	}
	var digits, check int64
	for r := int64(0); r < rounds; r++ {
		for _, n := range numbers {
			s := smallestNumber(n)
			digits += int64(len(s))
			for i := 0; i < len(s); i++ {
				check = (check*31 + int64(s[i]) + r) % 1000000007
			}
		}
	}
	fmt.Printf("%d numbers, %d rounds: %d digits, checksum %d\n", count, rounds, digits, check)
}
