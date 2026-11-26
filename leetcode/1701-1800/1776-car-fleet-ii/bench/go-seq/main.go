// LeetCode #1776: Car Fleet II -- the bench in Go, mirroring
// get_collision_times.kara: a stack of the cars ahead from the right.
package main

import (
	"fmt"
	"math"
)

func catchTime(cars [][]int32, i, j int) float64 {
	return float64(cars[j][0]-cars[i][0]) / float64(cars[i][1]-cars[j][1])
}

func getCollisionTimes(cars [][]int32) []float64 {
	n := len(cars)
	answer := make([]float64, n)
	for i := range answer {
		answer[i] = -1.0
	}
	stack := []int{}
	for i := n - 1; i >= 0; i-- {
		for len(stack) > 0 {
			j := stack[len(stack)-1]
			if cars[i][1] <= cars[j][1] || (answer[j] > 0.0 && catchTime(cars, i, j) >= answer[j]) {
				stack = stack[:len(stack)-1]
			} else {
				break
			}
		}
		if len(stack) > 0 {
			answer[i] = catchTime(cars, i, stack[len(stack)-1])
		}
		stack = append(stack, i)
	}
	return answer
}

var seed int64 = 1776

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][][]int32, 0, 20)
	for l := 0; l < 20; l++ {
		fastest := int64(100)
		if l%2 == 0 {
			fastest = 1000000
		}
		cars := make([][]int32, 0, 100000)
		var position int64
		for k := 0; k < 100000; k++ {
			position += 1 + nextRandom()%10
			speed := 1 + nextRandom()%fastest
			cars = append(cars, []int32{int32(position), int32(speed)})
		}
		lists = append(lists, cars)
	}
	var check int64
	for call := int64(0); call < 200; call++ {
		answer := getCollisionTimes(lists[(check+call)%20])
		t := answer[check%100000]
		check = (check*31 + int64(math.Floor(t*100000.0+0.5)) + 100001) % 1000000007
	}
	fmt.Printf("200 calls over 20 lists: checksum %d\n", check)
}
