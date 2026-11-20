// LeetCode #1742: Maximum Number of Balls in a Box -- the bench
// (balls.kara in Go): a count for every digit sum.
package main

import "fmt"

func countBalls(lowLimit, highLimit int32) int32 {
	var boxes [46]int32
	for ball := lowLimit; ball <= highLimit; ball++ {
		rest, sum := ball, int32(0)
		for rest > 0 {
			sum += rest % 10
			rest /= 10
		}
		boxes[sum]++
	}
	best := boxes[0]
	for _, b := range boxes {
		best = max(best, b)
	}
	return best
}

var seed int64 = 1742

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	const count, rounds = 200, 20
	lows := make([]int32, count)
	highs := make([]int32, count)
	for i := 0; i < count; i++ {
		a := wide()%100000 + 1
		b := wide()%100000 + 1
		lows[i], highs[i] = int32(min(a, b)), int32(max(a, b))
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for i := 0; i < count; i++ {
			answer := int64(countBalls(lows[i], highs[i]))
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d ranges inside 1 to 100000, %d rounds: largest boxes sum to %d, checksum %d\n", count, rounds, sum, check)
}
