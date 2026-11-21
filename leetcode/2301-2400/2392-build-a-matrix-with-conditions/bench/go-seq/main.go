// LeetCode #2392: Build a Matrix With Conditions -- the bench, the ★ arm
// in Go: Kahn's algorithm for the rows and again for the columns.
package main

import "fmt"

var seed int64 = 2392

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func conditions(k, count int64) [][2]int64 {
	order := make([]int64, k)
	for i := range order {
		order[i] = int64(i) + 1
	}
	for i := int64(1); i < k; i++ {
		j := nextRandom() % (i + 1)
		order[i], order[j] = order[j], order[i]
	}
	out := make([][2]int64, count)
	for n := range out {
		a := nextRandom() % k
		b := nextRandom() % (k - 1)
		if b >= a {
			b++
		}
		lo, hi := a, b
		if b < a {
			lo, hi = b, a
		}
		out[n] = [2]int64{order[lo], order[hi]}
	}
	return out
}

func order(k int64, edges [][2]int64) []int64 {
	next := make([][]int64, k+1)
	into := make([]int64, k+1)
	for _, e := range edges {
		next[e[0]] = append(next[e[0]], e[1])
		into[e[1]]++
	}
	queue := []int64{}
	for v := int64(1); v <= k; v++ {
		if into[v] == 0 {
			queue = append(queue, v)
		}
	}
	taken := []int64{}
	for head := 0; head < len(queue); head++ {
		v := queue[head]
		taken = append(taken, v)
		for _, w := range next[v] {
			into[w]--
			if into[w] == 0 {
				queue = append(queue, w)
			}
		}
	}
	return taken
}

func buildMatrix(k int64, rows, cols [][2]int64) [][]int64 {
	byRow := order(k, rows)
	byCol := order(k, cols)
	if int64(len(byRow)) < k || int64(len(byCol)) < k {
		return nil
	}
	colOf := make([]int64, k+1)
	for c, v := range byCol {
		colOf[v] = int64(c)
	}
	m := make([][]int64, k)
	for r := range m {
		m[r] = make([]int64, k)
	}
	for r, v := range byRow {
		m[r][colOf[v]] = v
	}
	return m
}

func main() {
	rows := make([][][2]int64, 20)
	cols := make([][][2]int64, 20)
	for i := 0; i < 20; i++ {
		rows[i] = conditions(200, 4000)
		cols[i] = conditions(200, 4000)
	}
	var check int64
	for p := int64(0); p < 500; p++ {
		for i := 0; i < 20; i++ {
			m := buildMatrix(200, rows[i], cols[i])
			for r := int64(0); r < 200; r++ {
				for c := int64(0); c < 200; c++ {
					if m[r][c] > 0 {
						check = (check*31 + m[r][c]*(r*200+c) + p) % 1000000007
					}
				}
			}
		}
	}
	fmt.Printf("500 passes over 20 matrices of k = 200: checksum %d\n", check)
}
