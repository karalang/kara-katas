// LeetCode #1652: Defuse the Bomb -- the bench's Go mirror: the ★ arm on
// 400 random codes of 100000 numbers from 1 to 100, each with a k from
// -99999 to 99999, all drawn first.
package main

import "fmt"

func decrypt(code []int32, k int32) []int32 {
	n := int64(len(code))
	answer := make([]int32, n)
	if k == 0 {
		return answer
	}
	kk := int64(k)
	var start, end int64
	if kk > 0 {
		start, end = 1, kk
	} else {
		start, end = n+kk, n-1
	}
	var sum int32
	for j := start; j <= end; j++ {
		sum += code[j%n]
	}
	for i := int64(0); i < n; i++ {
		answer[i] = sum
		sum -= code[start%n]
		start++
		end++
		sum += code[end%n]
	}
	return answer
}

var seed int64 = 1652

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type problem struct {
	code []int32
	k    int32
}

func main() {
	const n = 100000
	codes := make([]problem, 0, 400)
	for c := 0; c < 400; c++ {
		code := make([]int32, n)
		for i := range code {
			code[i] = int32(nextRandom()%100 + 1)
		}
		k := int32(nextRandom()%(2*n-1) - (n - 1))
		codes = append(codes, problem{code, k})
	}
	var check, total int64
	for _, p := range codes {
		for _, x := range decrypt(p.code, p.k) {
			total += int64(x)
			check = (check*31 + int64(x) + 1) % 1000000007
		}
	}
	fmt.Printf("400 codes of 100000 numbers: answers sum to %d, checksum %d\n", total, check)
}
