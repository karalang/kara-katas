// LeetCode #990: Satisfiability of Equality Equations -- bench, the ★
// arm (union-find with path halving), the same algorithm and workload
// as equations_possible.kara.
package main

import "fmt"

func find(parent []int64, x int64) int64 {
	for parent[x] != x {
		parent[x] = parent[parent[x]]
		x = parent[x]
	}
	return x
}

func equationsPossible(equations []string) bool {
	parent := make([]int64, 26)
	for i := range parent {
		parent[i] = int64(i)
	}
	for _, e := range equations {
		if e[1] == '=' {
			a := find(parent, int64(e[0])-97)
			b := find(parent, int64(e[3])-97)
			parent[a] = b
		}
	}
	for _, e := range equations {
		if e[1] == '!' && find(parent, int64(e[0])-97) == find(parent, int64(e[3])-97) {
			return false
		}
	}
	return true
}

var seed int64 = 990

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomEquations(n int, unequal int64) []string {
	out := make([]string, 0, n)
	for i := 0; i < n; i++ {
		a := string(rune(97 + nextRandom()%26))
		op := "=="
		if nextRandom()%256 < unequal {
			op = "!="
		}
		b := string(rune(97 + nextRandom()%26))
		out = append(out, a+op+b)
	}
	return out
}

func main() {
	rounds := 6000
	sets := make([][]string, 20)
	for i := range sets {
		sets[i] = randomEquations(500, int64(i%2))
	}
	var sat, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 20; i++ {
			ok := equationsPossible(sets[(r+i)%20])
			if ok {
				sat++
			}
			if ok {
				check = (check*31 + 2) % 1000000007
			} else {
				check = (check*31 + 1) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds over 20 sets of 500 equations: %d satisfiable, checksum %d\n", rounds, sat, check)
}
