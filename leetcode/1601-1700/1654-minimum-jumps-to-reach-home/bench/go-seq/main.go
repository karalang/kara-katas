// LeetCode #1654: Minimum Jumps to Reach Home -- the bench's Go mirror:
// the ★ arm on 5000 random problems with a, b and x up to 2000 and up to
// 1000 forbidden positions, all drawn first.
package main

import "fmt"

type state struct {
	p     int64
	back  bool
	jumps int32
}

func minimumJumps(forbidden []int32, a32, b32, x32 int32) int32 {
	a, b, x := int64(a32), int64(b32), int64(x32)
	var furthest int64
	for _, f := range forbidden {
		furthest = max(furthest, int64(f))
	}
	limit := max(x, furthest) + a + b
	blocked := make([]bool, limit+1)
	for _, f := range forbidden {
		blocked[f] = true
	}
	seen := make([][2]bool, limit+1)
	queue := []state{{0, false, 0}}
	seen[0][0] = true
	for len(queue) > 0 {
		s := queue[0]
		queue = queue[1:]
		if s.p == x {
			return s.jumps
		}
		forward := s.p + a
		if forward <= limit && !blocked[forward] && !seen[forward][0] {
			seen[forward][0] = true
			queue = append(queue, state{forward, false, s.jumps + 1})
		}
		backward := s.p - b
		if !s.back && backward >= 0 && !blocked[backward] && !seen[backward][1] {
			seen[backward][1] = true
			queue = append(queue, state{backward, true, s.jumps + 1})
		}
	}
	return -1
}

var seed int64 = 1654

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type problem struct {
	forbidden []int32
	a, b, x   int32
}

func main() {
	problems := make([]problem, 0, 5000)
	for k := 0; k < 5000; k++ {
		a := int32(nextRandom()%2000 + 1)
		b := int32(nextRandom()%2000 + 1)
		x := int32(nextRandom() % 2001)
		m := nextRandom() % 1001
		taken := make([]bool, 2001)
		forbidden := []int32{}
		for i := int64(0); i < m; i++ {
			f := int32(nextRandom()%2000 + 1)
			if f != x && !taken[f] {
				taken[f] = true
				forbidden = append(forbidden, f)
			}
		}
		problems = append(problems, problem{forbidden, a, b, x})
	}
	var check, total, unreachable int64
	for _, pr := range problems {
		answer := int64(minimumJumps(pr.forbidden, pr.a, pr.b, pr.x))
		if answer < 0 {
			unreachable++
		}
		total += answer
		check = (check*31 + answer + 2) % 1000000007
	}
	fmt.Printf("5000 problems up to 2000: jumps sum to %d, %d unreachable, checksum %d\n", total, unreachable, check)
}
