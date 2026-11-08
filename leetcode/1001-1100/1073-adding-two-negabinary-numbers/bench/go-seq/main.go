// LeetCode #1073: Adding Two Negabinary Numbers -- the benchmark's Go
// mirror of negabinary.kara: the same addition from the low end with a
// carry, over 2000 pairs of numbers built once, each added 20 times.
package main

import "fmt"

func addNegabinary(a, b []int64) []int64 {
	i, j, carry := len(a)-1, len(b)-1, int64(0)
	var digits []int64
	for i >= 0 || j >= 0 || carry != 0 {
		s := carry
		if i >= 0 {
			s += a[i]
			i--
		}
		if j >= 0 {
			s += b[j]
			j--
		}
		digits = append(digits, s&1)
		carry = -(s >> 1)
	}
	for len(digits) > 1 && digits[len(digits)-1] == 0 {
		digits = digits[:len(digits)-1]
	}
	for l, r := 0, len(digits)-1; l < r; l, r = l+1, r-1 {
		digits[l], digits[r] = digits[r], digits[l]
	}
	return digits
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomNumber(longest int64, seed *int64) []int64 {
	n := nextRandom(seed)%longest + 1
	if n == 1 {
		return []int64{nextRandom(seed) % 2}
	}
	digits := []int64{1}
	for k := int64(1); k < n; k++ {
		digits = append(digits, nextRandom(seed)%2)
	}
	return digits
}

func main() {
	seed := int64(1073)
	as := make([][]int64, 0, 2000)
	bs := make([][]int64, 0, 2000)
	for k := 0; k < 2000; k++ {
		as = append(as, randomNumber(1000, &seed))
		bs = append(bs, randomNumber(1000, &seed))
	}
	var total, check int64
	for r := 0; r < 20; r++ {
		for k := range as {
			x := addNegabinary(as[k], bs[k])
			total += int64(len(x))
			check = (check*31 + int64(len(x)) + x[len(x)/2]) % 1000000007
		}
	}
	fmt.Printf("40000 calls: %d digits, checksum %d\n", total, check)
}
