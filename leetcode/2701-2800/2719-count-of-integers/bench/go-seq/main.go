// LeetCode #2719: Count of Integers -- the bench (integers.kara in Go): the
// good numbers up to each bound by a digit-by-digit recursion, a free
// place's count remembered by place and digit sum.
package main

import "fmt"

const mod = 1000000007

func walk(digits []int64, place int, sum int64, tight bool, minSum, maxSum int64, memo [][]int64) int64 {
	if sum > maxSum {
		return 0
	}
	if place == len(digits) {
		if sum >= minSum {
			return 1
		}
		return 0
	}
	if !tight && memo[place][sum] >= 0 {
		return memo[place][sum]
	}
	top := int64(9)
	if tight {
		top = digits[place]
	}
	var ways int64
	for d := int64(0); d <= top; d++ {
		ways = (ways + walk(digits, place+1, sum+d, tight && d == top, minSum, maxSum, memo)) % mod
	}
	if !tight {
		memo[place][sum] = ways
	}
	return ways
}

func goodUpTo(bound string, minSum, maxSum int64) int64 {
	digits := make([]int64, len(bound))
	for i := range bound {
		digits[i] = int64(bound[i] - '0')
	}
	memo := make([][]int64, len(digits))
	for i := range memo {
		memo[i] = make([]int64, maxSum+1)
		for s := range memo[i] {
			memo[i][s] = -1
		}
	}
	return walk(digits, 0, 0, true, minSum, maxSum, memo)
}

func count(num1, num2 string, minSum, maxSum int64) int64 {
	var own int64
	for i := range num1 {
		own += int64(num1[i] - '0')
	}
	var itself int64
	if minSum <= own && own <= maxSum {
		itself = 1
	}
	return (goodUpTo(num2, minSum, maxSum) - goodUpTo(num1, minSum, maxSum) + itself + mod) % mod
}

var seed int64 = 2719

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type problem struct {
	num1, num2 string
	low, high  int64
}

func main() {
	ranges, rounds := 300, 10
	problems := make([]problem, 0, ranges)
	for k := 0; k < ranges; k++ {
		a := []byte{byte('1' + nextRandom()%4)}
		b := []byte{byte('5' + nextRandom()%5)}
		for i := 1; i < 22; i++ {
			a = append(a, byte('0'+nextRandom()%10))
			b = append(b, byte('0'+nextRandom()%10))
		}
		low := nextRandom()%400 + 1
		high := low + nextRandom()%(401-low)
		problems = append(problems, problem{string(a), string(b), low, high})
	}
	var sum, check int64
	for r := 0; r < rounds; r++ {
		for _, p := range problems {
			found := count(p.num1, p.num2, p.low, p.high)
			sum += found
			check = (check*31 + found + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d ranges of 22 digits, %d rounds: counts mod p sum to %d, checksum %d\n", ranges, rounds, sum, check)
}
