// LeetCode #690: Employee Importance -- breadth first, by id. Bench.
//
// 30 companies of 2,000 people, ids 1 to 2000 in random order, each
// person under a random earlier one, are built once, with 100 random
// people to ask about in each; then 80 rounds ask about all of them.

package main

import "fmt"

type Employee struct {
	id           int64
	importance   int64
	subordinates []int64
}

func getImportance(employees []Employee, id int64) int64 {
	at := make([]int64, 2001)
	for i := range at {
		at[i] = -1
	}
	for i := range employees {
		at[employees[i].id] = int64(i)
	}
	// A slice used as a queue: taken from the front, added at the back.
	queue := []int64{id}
	var sum int64
	for len(queue) > 0 {
		next := queue[0]
		queue = queue[1:]
		e := &employees[at[next]]
		sum += e.importance
		queue = append(queue, e.subordinates...)
	}
	return sum
}

var seed int64 = 690

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds, size = 30, 80, 2000
	companies := make([][]Employee, count)
	questions := make([][]int64, count)
	for c := 0; c < count; c++ {
		ids := make([]int64, size)
		for i := range ids {
			ids[i] = int64(i + 1)
		}
		for i := int64(0); i < size; i++ {
			j := i + nextRandom()%(size-i)
			ids[i], ids[j] = ids[j], ids[i]
		}
		subs := make([][]int64, size)
		for i := int64(1); i < size; i++ {
			boss := nextRandom() % i
			subs[boss] = append(subs[boss], ids[i])
		}
		company := make([]Employee, size)
		for i := 0; i < size; i++ {
			importance := nextRandom()%201 - 100
			company[i] = Employee{ids[i], importance, append([]int64(nil), subs[i]...)}
		}
		companies[c] = company
		ask := make([]int64, 100)
		for q := range ask {
			ask[q] = 1 + nextRandom()%size
		}
		questions[c] = ask
	}
	var sum int64
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < count; c++ {
			for q := 0; q < 100; q++ {
				got := getImportance(companies[c], questions[c][q])
				sum = (sum*31 + got + 1000000 + r) % 1000000007
			}
		}
	}
	fmt.Printf("%d questions answered, checksum %d\n", count*rounds*100, sum)
}
