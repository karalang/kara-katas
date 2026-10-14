// LeetCode #625: Minimum Factorization -- Go mirror of the Kāra bench.
//
// The ★ arm's greedy from the largest digit over the same numbers and
// rounds.
package main

import "fmt"

func smallestFactorization(num int64) int64 {
	if num < 10 {
		return num
	}
	rest, answer, place := num, int64(0), int64(1)
	for d := int64(9); d >= 2; d-- {
		for rest%d == 0 {
			rest /= d
			answer += d * place
			place *= 10
			if answer > 2147483647 {
				return 0
			}
		}
	}
	if rest == 1 {
		return answer
	}
	return 0
}

var seed int64 = 625

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomNumbers(count int64) []int64 {
	numbers := make([]int64, 0, count)
	for i := int64(0); i < count; i++ {
		if i%2 == 0 {
			product := int64(1)
			n := 1 + nextRandom()%10
			for j := int64(0); j < n; j++ {
				d := 2 + nextRandom()%8
				if product*d <= 2147483647 {
					product *= d
				}
			}
			numbers = append(numbers, product)
		} else {
			high := nextRandom()
			low := nextRandom()
			numbers = append(numbers, 1+(high*65536+low)%2147483647)
		}
	}
	return numbers
}

func main() {
	const count = 200000
	const rounds = 50
	numbers := randomNumbers(count)
	var found, checksum int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			a := smallestFactorization(numbers[i])
			if a != 0 {
				found++
			}
			checksum = (checksum*31 + a) % 1000000007
		}
	}
	fmt.Printf("%d numbers, %d rounds: %d answers, checksum %d\n", count, rounds, found, checksum)
}
