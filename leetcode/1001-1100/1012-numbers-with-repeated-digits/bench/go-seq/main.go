// LeetCode #1012 bench: the ★ arm (counting arrangements) over 100,000
// values of n up to a billion, drawn once; each of 40 rounds counts every
// value shifted by its own amount and folds each count into a checksum.

package main

import "fmt"

func numDupDigitsAtMostN(n int64) int64 {
	return n - distinctUpTo(n)
}

func distinctUpTo(n int64) int64 {
	digits := []int64{}
	rest := n
	for rest > 0 {
		digits = append(digits, rest%10)
		rest /= 10
	}
	for i, j := 0, len(digits)-1; i < j; i, j = i+1, j-1 {
		digits[i], digits[j] = digits[j], digits[i]
	}
	length := int64(len(digits))
	count := int64(0)
	for k := int64(1); k < length; k++ {
		count += 9 * arrangements(9, k-1)
	}
	seen := make([]bool, 10)
	for i := int64(0); i < length; i++ {
		d := digits[i]
		lowest := int64(0)
		if i == 0 {
			lowest = 1
		}
		for smaller := lowest; smaller < d; smaller++ {
			if !seen[smaller] {
				count += arrangements(9-i, length-i-1)
			}
		}
		if seen[d] {
			return count
		}
		seen[d] = true
	}
	return count + 1
}

func arrangements(free, slots int64) int64 {
	ways := int64(1)
	for j := int64(0); j < slots; j++ {
		ways *= free - j
	}
	return ways
}

var seed int64 = 1012

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count := 100000
	rounds := 40
	values := make([]int64, count)
	for i := 0; i < count; i++ {
		hi := nextRandom()
		lo := nextRandom()
		values[i] = (hi*32768 + lo) % 1000000000
	}
	check := int64(0)
	for r := 0; r < rounds; r++ {
		for k := 0; k < count; k++ {
			n := (values[k]+int64(r)*7919)%1000000000 + 1
			check = (check*31 + numDupDigitsAtMostN(n)) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d values of n: checksum %d\n", rounds, count, check)
}
