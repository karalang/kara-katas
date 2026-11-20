// LeetCode #1279 bench, in Go: the ★ arm (the green road behind a
// `sync.Mutex`, held while a car turns its light and crosses) over 2000
// runs of 20 cars, a goroutine for each car, on random roads and started
// in a random order; each run's log judged by the statement read literally.
package main

import (
	"fmt"
	"sync"
)

type event struct{ kind, x int64 }

type TrafficLight struct {
	lock  sync.Mutex
	green int64
}

func (t *TrafficLight) carArrived(carID, roadID, direction int64, turnGreen, crossCar func()) {
	t.lock.Lock()
	defer t.lock.Unlock()
	if t.green != roadID {
		turnGreen()
		t.green = roadID
	}
	crossCar()
}

var seed int64 = 1279

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func run(directions []int64, order []int) []event {
	light := &TrafficLight{green: 1}
	var lock sync.Mutex
	var log []event
	push := func(e event) {
		lock.Lock()
		log = append(log, e)
		lock.Unlock()
	}
	var wg sync.WaitGroup
	for _, i := range order {
		direction := directions[i]
		road := int64(2)
		if direction <= 2 {
			road = 1
		}
		wg.Add(1)
		go func(i int, road, direction int64) {
			defer wg.Done()
			light.carArrived(int64(i), road, direction, func() { push(event{0, road}) }, func() { push(event{1, int64(i)}) })
		}(i, road, direction)
	}
	wg.Wait()
	return log
}

func judge(directions []int64, log []event) bool {
	green := int64(1)
	crossed := make([]bool, len(directions))
	for _, e := range log {
		if e.kind == 0 {
			if e.x == green {
				return false
			}
			green = e.x
		} else {
			road := int64(2)
			if directions[e.x] <= 2 {
				road = 1
			}
			if road != green || crossed[e.x] {
				return false
			}
			crossed[e.x] = true
		}
	}
	for _, c := range crossed {
		if !c {
			return false
		}
	}
	return true
}

func main() {
	cars, valid := 0, 0
	for r := 0; r < 2000; r++ {
		directions := make([]int64, 20)
		for i := range directions {
			directions[i] = nextRandom()%4 + 1
		}
		order := make([]int, 20)
		for i := range order {
			order[i] = i
		}
		for i := 19; i >= 1; i-- {
			j := int(nextRandom() % int64(i+1))
			order[i], order[j] = order[j], order[i]
		}
		log := run(directions, order)
		for _, e := range log {
			if e.kind == 1 {
				cars++
			}
		}
		if judge(directions, log) {
			valid++
		}
	}
	fmt.Printf("2000 runs of 20 cars: %d cars crossed, %d valid\n", cars, valid)
}
