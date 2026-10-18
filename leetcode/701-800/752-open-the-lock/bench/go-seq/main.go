// LeetCode 752 — Open the Lock, bench: the ★ arm (breadth-first over
// numbers) against 500 dead ends that keep changing. Mirrors open_lock.kara.
package main

import (
	"fmt"
	"strconv"
)

func openLock(deadends []string, target string) int64 {
	blocked := make([]bool, 10000)
	for _, d := range deadends {
		v, _ := strconv.Atoi(d)
		blocked[v] = true
	}
	goal, _ := strconv.Atoi(target)
	if blocked[0] {
		return -1
	}
	dist := make([]int64, 10000)
	for i := range dist {
		dist[i] = -1
	}
	dist[0] = 0
	queue := []int{0}
	for len(queue) > 0 {
		at := queue[0]
		queue = queue[1:]
		if at == goal {
			return dist[at]
		}
		place := 1
		for w := 0; w < 4; w++ {
			digit := at / place % 10
			for _, step := range [2]int{1, 9} {
				next := at + ((digit+step)%10-digit)*place
				if !blocked[next] && dist[next] == -1 {
					dist[next] = dist[at] + 1
					queue = append(queue, next)
				}
			}
			place *= 10
		}
	}
	return -1
}

var seed int64 = 752

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func four(x int64) string {
	return fmt.Sprintf("%d%d%d%d", x/1000, x/100%10, x/10%10, x%10)
}

func main() {
	const rounds = 3000
	deadends := make([]string, 500)
	for i := range deadends {
		deadends[i] = four(1 + nextRandom()%9999)
	}
	var total, stuck int64
	for r := 0; r < rounds; r++ {
		for k := 0; k < 5; k++ {
			i := nextRandom() % 500
			deadends[i] = four(1 + nextRandom()%9999)
		}
		target := four(nextRandom() % 10000)
		turns := openLock(deadends, target)
		if turns == -1 {
			stuck++
		} else {
			total += turns
		}
	}
	fmt.Printf("%d locks with 500 dead ends: %d cannot open, the rest take %d turns in all\n", rounds, stuck, total)
}
