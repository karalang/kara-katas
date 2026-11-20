// LeetCode #1226 bench: the ★ arm in Go over the same 3 runs of n = 50000
// as the Kāra bench: a goroutine per philosopher, a `sync.Mutex` for each
// fork, the lower-numbered fork taken first, the log under its own mutex.
package main

import (
	"fmt"
	"sync"
)

type entry struct{ p, fork, op int }

type DiningPhilosophers struct {
	forks [5]sync.Mutex
}

func (t *DiningPhilosophers) wantsToEat(philosopher int, pickLeftFork, pickRightFork, eat, putLeftFork, putRightFork func()) {
	left, right := philosopher, (philosopher+4)%5
	first, second := min(left, right), max(left, right)
	t.forks[first].Lock()
	t.forks[second].Lock()
	pickLeftFork()
	pickRightFork()
	eat()
	putLeftFork()
	putRightFork()
	t.forks[second].Unlock()
	t.forks[first].Unlock()
}

func run(n int, order []int) []entry {
	var table DiningPhilosophers
	var lock sync.Mutex
	var log []entry
	push := func(e entry) {
		lock.Lock()
		log = append(log, e)
		lock.Unlock()
	}
	var wg sync.WaitGroup
	for _, p := range order {
		wg.Add(1)
		go func(p int) {
			defer wg.Done()
			for i := 0; i < n; i++ {
				table.wantsToEat(p,
					func() { push(entry{p, 1, 1}) },
					func() { push(entry{p, 2, 1}) },
					func() { push(entry{p, 0, 3}) },
					func() { push(entry{p, 1, 2}) },
					func() { push(entry{p, 2, 2}) })
			}
		}(p)
	}
	wg.Wait()
	return log
}

func judge(n int, log []entry) string {
	holder := [5]int{-1, -1, -1, -1, -1}
	var meals [5]int
	for _, e := range log {
		f := e.p
		if e.fork != 1 {
			f = (e.p + 4) % 5
		}
		switch e.op {
		case 1:
			if holder[f] != -1 {
				return fmt.Sprintf("philosopher %d picks up fork %d, held by %d", e.p, f, holder[f])
			}
			holder[f] = e.p
		case 2:
			if holder[f] != e.p {
				return fmt.Sprintf("philosopher %d puts down fork %d, not holding it", e.p, f)
			}
			holder[f] = -1
		default:
			if holder[e.p] != e.p || holder[(e.p+4)%5] != e.p {
				return fmt.Sprintf("philosopher %d eats without both forks", e.p)
			}
			meals[e.p]++
		}
	}
	for k := 0; k < 5; k++ {
		if meals[k] != n {
			return fmt.Sprintf("meals %v", meals)
		}
		if holder[k] != -1 {
			return fmt.Sprintf("forks left held %v", holder)
		}
	}
	return "valid"
}

func main() {
	calls, valid := 0, 0
	for _, order := range [][]int{{0, 1, 2, 3, 4}, {4, 3, 2, 1, 0}, {2, 0, 4, 1, 3}} {
		log := run(50000, order)
		calls += len(log)
		if judge(50000, log) == "valid" {
			valid++
		}
	}
	fmt.Printf("3 runs of n = 50000: %d calls, %d valid\n", calls, valid)
}
