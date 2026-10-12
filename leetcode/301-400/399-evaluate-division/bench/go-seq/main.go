// Benchmark for #399: mirror of evaluate_division.kara (union-find with weights).
package main

import "fmt"

func find(parent []int, weight []float64, i int) int {
	p := parent[i]
	if p == i {
		return i
	}
	root := find(parent, weight, p)
	weight[i] = weight[i] * weight[p]
	parent[i] = root
	return root
}

type pair struct{ a, b string }

func calcEquation(equations []pair, values []float64, queries []pair) []float64 {
	index := map[string]int{}
	var parent []int
	var weight []float64
	intern := func(name string) int {
		if i, ok := index[name]; ok {
			return i
		}
		i := len(parent)
		index[name] = i
		parent = append(parent, i)
		weight = append(weight, 1.0)
		return i
	}
	for k := range equations {
		a := intern(equations[k].a)
		b := intern(equations[k].b)
		ra := find(parent, weight, a)
		rb := find(parent, weight, b)
		if ra != rb {
			weight[ra] = values[k] * weight[b] / weight[a]
			parent[ra] = rb
		}
	}
	answers := make([]float64, 0, len(queries))
	for _, q := range queries {
		answer := -1.0
		if i, ok := index[q.a]; ok {
			if j, ok := index[q.b]; ok {
				if find(parent, weight, i) == find(parent, weight, j) {
					answer = weight[i] / weight[j]
				}
			}
		}
		answers = append(answers, answer)
	}
	return answers
}

var seed int64 = 3991

func step() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func pow2(k int64) float64 {
	x := 1.0
	n := k
	if n < 0 {
		n = -n
	}
	for i := int64(0); i < n; i++ {
		x = x * 2.0
	}
	if k < 0 {
		return 1.0 / x
	}
	return x
}

func exponent(x float64) int64 {
	v := x
	var k int64
	for v >= 2.0 {
		v = v / 2.0
		k++
	}
	for v < 1.0 {
		v = v * 2.0
		k--
	}
	return k
}

func main() {
	systems := 100000
	var answered, checksum int64
	for s := 0; s < systems; s++ {
		m := 2 + step()%39
		hidden := make([]int64, m)
		for i := range hidden {
			hidden[i] = step()%9 - 4
		}
		var equations []pair
		var values []float64
		for e := 0; e < 20; e++ {
			a := step() % m
			b := step() % m
			equations = append(equations, pair{fmt.Sprintf("v%d", a), fmt.Sprintf("v%d", b)})
			values = append(values, pow2(hidden[a]-hidden[b]))
		}
		var queries []pair
		for q := 0; q < 20; q++ {
			a := step() % (m + 2)
			b := step() % (m + 2)
			queries = append(queries, pair{fmt.Sprintf("v%d", a), fmt.Sprintf("v%d", b)})
		}
		for _, x := range calcEquation(equations, values, queries) {
			if x < 0.0 {
				checksum = (checksum*31 + 1) % 1000000007
			} else {
				answered++
				checksum = (checksum*31 + exponent(x) + 50) % 1000000007
			}
		}
	}
	fmt.Printf("%d systems: %d answered, checksum %d\n", systems, answered, checksum)
}
