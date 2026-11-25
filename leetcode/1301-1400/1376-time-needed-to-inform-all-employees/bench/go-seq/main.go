// LeetCode #1376 bench -- Go: the ★ arm: each manager's reports in a
// slice, then a breadth-first walk down from the head, each employee
// hearing the news when the manager heard it plus the manager's inform
// time.
package main

import "fmt"

func numOfMinutes(n int, headID int, manager []int32, informTime []int32) int32 {
	reports := make([][]int, n)
	for i, m := range manager {
		if m >= 0 {
			reports[m] = append(reports[m], i)
		}
	}
	heard := make([]int32, n)
	queue := []int{headID}
	var latest int32
	for len(queue) > 0 {
		u := queue[0]
		queue = queue[1:]
		if heard[u] > latest {
			latest = heard[u]
		}
		for _, v := range reports[u] {
			heard[v] = heard[u] + informTime[u]
			queue = append(queue, v)
		}
	}
	return latest
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 10 companies of 10^5 employees, built once; then 200 rounds, each
	// giving one employee of one company a new inform time if it is a
	// manager, and timing that company (see the Kāra bench)
	const n = int64(100000)
	seed := int64(1376)
	heads := make([]int, 0, 10)
	managers := make([][]int32, 0, 10)
	informs := make([][]int32, 0, 10)
	for c := 0; c < 10; c++ {
		order := make([]int64, n)
		for i := range order {
			order[i] = int64(i)
		}
		for i := n - 1; i >= 1; i-- {
			j := nextRandom(&seed) % (i + 1)
			order[i], order[j] = order[j], order[i]
		}
		manager := make([]int32, n)
		inform := make([]int32, n)
		manager[order[0]] = -1
		for k := int64(1); k < n; k++ {
			m := order[nextRandom(&seed)%k]
			manager[order[k]] = int32(m)
			if inform[m] == 0 {
				inform[m] = int32(1 + nextRandom(&seed)%1000)
			}
		}
		heads = append(heads, int(order[0]))
		managers = append(managers, manager)
		informs = append(informs, inform)
	}
	check := int64(0)
	for r := int64(0); r < 200; r++ {
		c := check % 10
		e := (check / 10) % n
		if informs[c][e] > 0 {
			informs[c][e] = int32(1 + (check+r)%1000)
		}
		got := int64(numOfMinutes(int(n), heads[c], managers[c], informs[c]))
		check = (check*31 + got + r) % 1000000007
	}
	fmt.Printf("200 rounds over 10 companies of 100000 employees: checksum %d\n", check)
}
