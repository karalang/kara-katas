// LeetCode #2183: Count Array Pairs Divisible by K -- the benchmark's Go
// mirror of pairs_divisible.kara, over a slice.
package main

import "fmt"

func gcd(a, b int64) int64 {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func countPairs(nums []int64, k int64) int64 {
	byGcd := make([]int64, k+1)
	for _, x := range nums {
		byGcd[gcd(x, k)]++
	}
	var divisors []int64
	for d := int64(1); d*d <= k; d++ {
		if k%d == 0 {
			if byGcd[d] > 0 {
				divisors = append(divisors, d)
			}
			if d*d != k && byGcd[k/d] > 0 {
				divisors = append(divisors, k/d)
			}
		}
	}
	var pairs int64
	for a := 0; a < len(divisors); a++ {
		for b := a; b < len(divisors); b++ {
			g := divisors[a]
			h := divisors[b]
			if g*h%k == 0 {
				if a == b {
					pairs += byGcd[g] * (byGcd[g] - 1) / 2
				} else {
					pairs += byGcd[g] * byGcd[h]
				}
			}
		}
	}
	return pairs
}

var seed int64 = 2183

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func bigRandom() int64 {
	a := nextRandom()
	b := nextRandom()
	return a*32768 + b
}

func main() {
	row := make([]int64, 1000000)
	for i := range row {
		row[i] = bigRandom()%100000 + 1
	}
	var check int64
	for r := 0; r < 200; r++ {
		start := bigRandom() % 900001
		k := bigRandom()%100000 + 1
		found := countPairs(row[start:start+100000], k)
		check = (check*31 + found%1000000007) % 1000000007
	}
	fmt.Printf("200 solves: checksum %d\n", check)
}
