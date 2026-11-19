// LeetCode #1629: Slowest Key -- the bench's Go mirror: the ★ arm on 1000
// random problems of 1000 presses, all drawn first, each answered 100
// times.
package main

import "fmt"

func slowestKey(releaseTimes []int32, keysPressed string) byte {
	var previous, bestTime int32
	bestKey := byte('a')
	for i, time := range releaseTimes {
		duration, key := time-previous, keysPressed[i]
		if duration > bestTime || (duration == bestTime && key > bestKey) {
			bestTime, bestKey = duration, key
		}
		previous = time
	}
	return bestKey
}

var seed int64 = 1629

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	type problem struct {
		releaseTimes []int32
		keysPressed  string
	}
	problems := make([]problem, 1000)
	for p := range problems {
		times := make([]int32, 1000)
		keys := make([]byte, 1000)
		var time int64
		for i := range times {
			time += nextRandom()%1000 + 1
			times[i] = int32(time)
			keys[i] = byte('a' + nextRandom()%26)
		}
		problems[p] = problem{times, string(keys)}
	}
	var check int64
	for r := 0; r < 100; r++ {
		for _, p := range problems {
			key := slowestKey(p.releaseTimes, p.keysPressed)
			check = (check*31 + int64(key)) % 1000000007
		}
	}
	fmt.Printf("1000 problems of 1000 presses, answered 100 times: checksum %d\n", check)
}
