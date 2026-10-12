// Benchmark for #406: mirror of queue_reconstruction.kara (tallest first,
// each inserted at its k).
package main

import (
	"fmt"
	"sort"
)

type Person struct {
	h, k int64
}

func reconstructQueue(people []Person) []Person {
	sort.SliceStable(people, func(a, b int) bool {
		if people[a].h != people[b].h {
			return people[a].h > people[b].h
		}
		return people[a].k < people[b].k
	})
	queue := make([]Person, 0, len(people))
	for _, p := range people {
		queue = append(queue, Person{})
		copy(queue[p.k+1:], queue[p.k:])
		queue[p.k] = p
	}
	return queue
}

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	queues := 1000
	var n int64 = 2000
	var seed int64 = 406
	rebuilt := 0
	var checksum int64
	for t := 0; t < queues; t++ {
		var count [51]int64
		line := make([]Person, 0, n)
		for i := int64(0); i < n; i++ {
			h := 1 + step(&seed)%50
			var k int64
			for g := h; g < 51; g++ {
				k += count[g]
			}
			count[h]++
			line = append(line, Person{h, k})
		}
		people := make([]Person, n)
		copy(people, line)
		for i := n - 1; i >= 1; i-- {
			j := step(&seed) % (i + 1)
			people[i], people[j] = people[j], people[i]
		}
		q := reconstructQueue(people)
		same := true
		for i := range q {
			if q[i] != line[i] {
				same = false
			}
		}
		if same {
			rebuilt++
		}
		for i := range q {
			checksum = (checksum*31 + q[i].h*10000 + q[i].k) % 1000000007
		}
	}
	fmt.Printf("%d queues of %d people: %d rebuilt, checksum %d\n", queues, n, rebuilt, checksum)
}
