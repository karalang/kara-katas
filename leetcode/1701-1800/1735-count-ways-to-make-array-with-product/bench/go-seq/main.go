// LeetCode #1735: Count Ways to Make Array With Product -- the bench
// (ways.kara): the product over k's primes of C(n + e - 1, e), read off
// factorials and their inverses.
package main

import "fmt"

const mod = 1000000007

func power(base, exp int64) int64 {
	result := int64(1)
	b := base % mod
	e := exp
	for e > 0 {
		if e%2 == 1 {
			result = result * b % mod
		}
		b = b * b % mod
		e /= 2
	}
	return result
}

func waysToFillArray(queries [][]int32) []int32 {
	var top int64
	for _, q := range queries {
		if int64(q[0]) > top {
			top = int64(q[0])
		}
	}
	top += 14
	fact := make([]int64, top+1)
	fact[0] = 1
	for i := int64(1); i <= top; i++ {
		fact[i] = fact[i-1] * i % mod
	}
	inverse := make([]int64, top+1)
	inverse[top] = power(fact[top], mod-2)
	for i := top; i >= 1; i-- {
		inverse[i-1] = inverse[i] * i % mod
	}
	choose := func(m, r int64) int64 {
		return fact[m] * inverse[r] % mod * inverse[m-r] % mod
	}
	answers := make([]int32, 0)
	for _, q := range queries {
		n := int64(q[0])
		k := int64(q[1])
		ways := int64(1)
		for p := int64(2); p*p <= k; p++ {
			e := int64(0)
			for k%p == 0 {
				k /= p
				e++
			}
			ways = ways * choose(n+e-1, e) % mod
		}
		if k > 1 {
			ways = ways * n % mod
		}
		answers = append(answers, int32(ways))
	}
	return answers
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := 10
	var rounds int64 = 60
	q := 10000
	var seed int64 = 1735
	problems := make([][][]int32, 0, count)
	for p := 0; p < count; p++ {
		queries := make([][]int32, 0, q)
		for i := 0; i < q; i++ {
			n := int32(nextRandom(&seed)%10000 + 1)
			k := int32(nextRandom(&seed)%10000 + 1)
			queries = append(queries, []int32{n, k})
		}
		problems = append(problems, queries)
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, queries := range problems {
			answers := waysToFillArray(queries)
			sum += int64(answers[0])
			check = (check*31 + int64(answers[0]) + int64(answers[q/2]) + int64(answers[q-1]) + r) % 1000000007
		}
	}
	fmt.Printf("%d lists of %d queries, %d rounds: first answers sum to %d, checksum %d\n", count, q, rounds, sum, check)
}
