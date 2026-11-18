// LeetCode #1188: Design Bounded Blocking Queue -- the bench in Go: the ★
// arm's two counting semaphores and a lock. Go's standard library has no
// counting semaphore, so each is a count under a `sync.Mutex` with a
// `sync.Cond`.
package main

import (
	"fmt"
	"sync"
)

type Semaphore struct {
	mu      sync.Mutex
	freed   *sync.Cond
	permits int64
}

func NewSemaphore(permits int64) *Semaphore {
	s := &Semaphore{permits: permits}
	s.freed = sync.NewCond(&s.mu)
	return s
}

func (s *Semaphore) Acquire() {
	s.mu.Lock()
	for s.permits == 0 {
		s.freed.Wait()
	}
	s.permits--
	s.mu.Unlock()
}

func (s *Semaphore) Release() {
	s.mu.Lock()
	s.permits++
	s.mu.Unlock()
	s.freed.Signal()
}

type BoundedBlockingQueue struct {
	slots, items *Semaphore
	mu           sync.Mutex
	values       []int64
}

func NewBoundedBlockingQueue(capacity int64) *BoundedBlockingQueue {
	return &BoundedBlockingQueue{slots: NewSemaphore(capacity), items: NewSemaphore(0)}
}

func (q *BoundedBlockingQueue) Enqueue(element int64) {
	q.slots.Acquire()
	q.mu.Lock()
	q.values = append(q.values, element)
	q.mu.Unlock()
	q.items.Release()
}

func (q *BoundedBlockingQueue) Dequeue() int64 {
	q.items.Acquire()
	q.mu.Lock()
	element := q.values[0]
	q.values = q.values[1:]
	q.mu.Unlock()
	q.slots.Release()
	return element
}

func (q *BoundedBlockingQueue) Size() int64 {
	q.mu.Lock()
	defer q.mu.Unlock()
	return int64(len(q.values))
}

func run(round int64) int64 {
	queue := NewBoundedBlockingQueue(16)
	var total int64
	var totalMu sync.Mutex
	var wg sync.WaitGroup
	for p := int64(0); p < 4; p++ {
		wg.Add(1)
		go func(p int64) {
			defer wg.Done()
			for k := int64(0); k < 2500; k++ {
				queue.Enqueue((round*7919 + p*10007 + k*31) % 1000)
			}
		}(p)
	}
	for c := 0; c < 4; c++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			var sum int64
			for k := 0; k < 2500; k++ {
				sum += queue.Dequeue()
			}
			totalMu.Lock()
			total += sum
			totalMu.Unlock()
		}()
	}
	wg.Wait()
	return total + 1000*queue.Size()
}

func main() {
	rounds := int64(100)
	var check int64
	for round := int64(0); round < rounds; round++ {
		check = (check*131 + run(round)) % 1000000007
	}
	fmt.Printf("%d rounds of 4 producers and 4 consumers moving 10000 values through 16 places: checksum %d\n", rounds, check)
}
