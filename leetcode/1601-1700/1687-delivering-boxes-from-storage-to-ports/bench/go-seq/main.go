// LeetCode #1687: Delivering Boxes from Storage to Ports -- the bench's Go
// mirror: the ★ arm on 50 random problems of 100000 boxes, all drawn first,
// each answered 20 times. Go has no deque: a slice with a head index, since
// each start goes in once.
package main

import "fmt"

func deliver(boxes [][2]int32, maxBoxes, maxWeight int32) int32 {
	n := len(boxes)
	changes := make([]int32, n)
	weight := make([]int64, n+1)
	for k := 0; k < n; k++ {
		weight[k+1] = weight[k] + int64(boxes[k][1])
		if k > 0 {
			changes[k] = changes[k-1]
			if boxes[k][0] != boxes[k-1][0] {
				changes[k]++
			}
		}
	}
	trips := make([]int32, n+1)
	starts := make([]int, n)
	head, tail := 0, 0
	for i := 1; i <= n; i++ {
		j := i - 1
		cost := trips[j] - changes[j]
		for tail > head && trips[starts[tail-1]]-changes[starts[tail-1]] >= cost {
			tail--
		}
		starts[tail] = j
		tail++
		for tail > head && (int32(i-starts[head]) > maxBoxes || weight[i]-weight[starts[head]] > int64(maxWeight)) {
			head++
		}
		front := starts[head]
		trips[i] = trips[front] - changes[front] + changes[i-1] + 2
	}
	return trips[n]
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1687

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, size, rounds = 50, 100000, 20
	type problem struct {
		boxes               [][2]int32
		maxBoxes, maxWeight int32
	}
	problems := make([]problem, 0, count)
	for c := 0; c < count; c++ {
		portsCount := nextRandom()%100 + 1
		maxBoxes := int32(nextRandom()%1000 + 1)
		maxWeight := int32(nextRandom()%99001 + 1000)
		boxes := make([][2]int32, size)
		for i := range boxes {
			boxes[i][0] = int32(nextRandom()%portsCount + 1)
			boxes[i][1] = int32(nextRandom()%1000 + 1)
		}
		problems = append(problems, problem{boxes, maxBoxes, maxWeight})
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, p := range problems {
			answer := int64(deliver(p.boxes, p.maxBoxes, p.maxWeight))
			total += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d problems of %d boxes, %d rounds: %d trips, checksum %d\n", count, size, rounds, total, check)
}
