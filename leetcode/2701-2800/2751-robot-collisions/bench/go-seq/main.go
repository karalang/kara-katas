// LeetCode #2751: Robot Collisions -- the bench (robots.kara in Go): the
// robots in order of position, those moving right on a stack, and each
// robot moving left meeting the stack's top in turn.
package main

import (
	"cmp"
	"fmt"
	"slices"
)

func survivedRobotsHealths(positions, healths []int64, directions []byte) []int64 {
	n := len(positions)
	health := slices.Clone(healths)
	order := make([]int, n)
	for i := range order {
		order[i] = i
	}
	slices.SortFunc(order, func(a, b int) int { return cmp.Compare(positions[a], positions[b]) })
	rightward := []int{}
	for _, i := range order {
		if directions[i] == 'R' {
			rightward = append(rightward, i)
			continue
		}
		for health[i] > 0 && len(rightward) > 0 {
			top := rightward[len(rightward)-1]
			if health[top] < health[i] {
				health[top] = 0
				rightward = rightward[:len(rightward)-1]
				health[i]--
			} else if health[top] > health[i] {
				health[top]--
				health[i] = 0
			} else {
				health[top] = 0
				rightward = rightward[:len(rightward)-1]
				health[i] = 0
			}
		}
	}
	out := []int64{}
	for _, h := range health {
		if h > 0 {
			out = append(out, h)
		}
	}
	return out
}

var seed int64 = 2751

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type testCase struct {
	positions, healths []int64
	directions         []byte
}

func main() {
	const count, rounds = 10, 3
	const n = 100000
	cases := []testCase{}
	for k := 0; k < count; k++ {
		positions := make([]int64, n)
		for i := range positions {
			positions[i] = int64(i)*10000 + nextRandom()%10000 + 1
		}
		for i := int64(n - 1); i >= 1; i-- {
			hi := nextRandom()
			j := (hi*32768 + nextRandom()) % (i + 1)
			positions[i], positions[j] = positions[j], positions[i]
		}
		healths := make([]int64, n)
		for i := range healths {
			hi := nextRandom()
			healths[i] = (hi*32768+nextRandom())%1000000000 + 1
		}
		directions := make([]byte, n)
		for i := range directions {
			if nextRandom()%2 == 0 {
				directions[i] = 'L'
			} else {
				directions[i] = 'R'
			}
		}
		cases = append(cases, testCase{positions, healths, directions})
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, c := range cases {
			survivors := survivedRobotsHealths(c.positions, c.healths, c.directions)
			check = (check*31 + int64(len(survivors)) + r) % 1000000007
			for _, h := range survivors {
				sum += h
				check = (check*31 + h) % 1000000007
			}
		}
	}
	fmt.Printf("%d cases of 100000 robots, %d rounds: healths sum to %d, checksum %d\n", count, rounds, sum, check)
}
