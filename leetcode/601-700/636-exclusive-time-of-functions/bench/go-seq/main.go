// LeetCode #636: Exclusive Time of Functions -- benchmark, Go.
//
// The ★ arm: one stack of running functions and the time of the last
// event.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

func exclusiveTime(n int, logs []string) []int64 {
	total := make([]int64, n)
	var stack []int
	var prev int64
	for _, log := range logs {
		parts := strings.Split(log, ":")
		id, _ := strconv.Atoi(parts[0])
		t, _ := strconv.ParseInt(parts[2], 10, 64)
		if parts[1] == "start" {
			if len(stack) > 0 {
				total[stack[len(stack)-1]] += t - prev
			}
			stack = append(stack, id)
			prev = t
		} else {
			top := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			total[top] += t - prev + 1
			prev = t + 1
		}
	}
	return total
}

var seed int64 = 636

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func randomLogs(n, calls, gap int64) []string {
	var logs []string
	var stack []int64
	var started, startAt, endAt int64
	for started < calls || len(stack) > 0 {
		begin := started < calls && (len(stack) == 0 || nextRandom()%2 == 0)
		if begin {
			id := nextRandom() % n
			t := startAt + wide()%gap
			logs = append(logs, fmt.Sprintf("%d:start:%d", id, t))
			stack = append(stack, id)
			started++
			startAt = t + 1
			endAt = t
		} else {
			id := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			t := endAt + wide()%gap
			logs = append(logs, fmt.Sprintf("%d:end:%d", id, t))
			startAt = t + 1
			endAt = t + 1
		}
	}
	return logs
}

func main() {
	var inputs [][]string
	for i := 0; i < 10; i++ {
		inputs = append(inputs, randomLogs(100, 250, 3800000))
	}
	var sum, checksum int64
	for r := 0; r < 10000; r++ {
		for _, t := range exclusiveTime(100, inputs[r%10]) {
			sum += t
			checksum = (checksum*31 + t) % 1000000007
		}
	}
	fmt.Printf("10 inputs of 500 logs, 10000 rounds: total %d, checksum %d\n", sum, checksum)
}
