// LeetCode #2338: Count the Number of Ideal Arrays -- the bench, the ★ arm
// in Go: the strictly increasing divisor chains of each length counted
// level by level, each length k + 1 spread over the n places in
// C(n - 1, k) ways.
package main

import "fmt"

const modulus int64 = 1000000007
const longest = 14

func power(base, exp int64) int64 {
	result := int64(1)
	base %= modulus
	for exp > 0 {
		if exp%2 == 1 {
			result = result * base % modulus
		}
		base = base * base % modulus
		exp /= 2
	}
	return result
}

func binomials(m int64, count int) []int64 {
	out := []int64{1}
	for k := 1; k < count; k++ {
		next := out[k-1] * ((m - int64(k) + 1) % modulus) % modulus * power(int64(k), modulus-2) % modulus
		out = append(out, next)
	}
	return out
}

func idealArrays(n, maxValue int64) int64 {
	ways := binomials(n-1, longest)
	size := maxValue + 1
	ends := make([]int64, size)
	for v := range ends {
		ends[v] = 1
	}
	ends[0] = 0
	answer := int64(0)
	for k := 0; k < longest; k++ {
		total := int64(0)
		for v := int64(1); v < size; v++ {
			total = (total + ends[v]) % modulus
		}
		answer = (answer + total*ways[k]) % modulus
		following := make([]int64, size)
		for d := int64(1); d < size; d++ {
			if ends[d] != 0 {
				for m := 2 * d; m < size; m += d {
					following[m] = (following[m] + ends[d]) % modulus
				}
			}
		}
		ends = following
	}
	return answer
}

func scrambled(index int64) int64 {
	return index * 2654435761 % 2147483647
}

func main() {
	check := int64(0)
	for q := int64(0); q < 300; q++ {
		n := 2 + scrambled(q+1)%9999
		maxValue := 5000 + scrambled(q+1001)%5001
		check = (check*31 + idealArrays(n, maxValue)) % 1000000007
	}
	fmt.Printf("300 queries of n up to 10^4 and maxValue 5000 to 10^4: checksum %d\n", check)
}
