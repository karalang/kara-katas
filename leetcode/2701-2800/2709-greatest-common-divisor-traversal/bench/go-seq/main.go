// LeetCode #2709: Greatest Common Divisor Traversal -- the bench
// (traversal.kara in Go): a smallest-prime-factor sieve, and each index
// joined in a union-find to the first index seen with each of its
// primes.
package main

import "fmt"

func find(parent []int64, a int64) int64 {
	for parent[a] != a {
		parent[a] = parent[parent[a]]
		a = parent[a]
	}
	return a
}

func canTraverseAllPairs(nums []int64) bool {
	n := int64(len(nums))
	if n == 1 {
		return true
	}
	top := nums[0]
	for _, v := range nums {
		if v > top {
			top = v
		}
	}
	spf := make([]int64, top+1)
	for i := range spf {
		spf[i] = int64(i)
	}
	for p := int64(2); p*p <= top; p++ {
		if spf[p] == p {
			for m := p * p; m <= top; m += p {
				if spf[m] == m {
					spf[m] = p
				}
			}
		}
	}
	parent := make([]int64, n)
	for i := range parent {
		parent[i] = int64(i)
	}
	first := make([]int64, top+1)
	for i := range first {
		first[i] = -1
	}
	sets := n
	for i, v := range nums {
		if v == 1 {
			return false
		}
		rest := v
		for rest > 1 {
			q := spf[rest]
			for rest%q == 0 {
				rest /= q
			}
			if first[q] < 0 {
				first[q] = int64(i)
			} else {
				a, b := find(parent, int64(i)), find(parent, first[q])
				if a != b {
					parent[a] = b
					sets--
				}
			}
		}
	}
	return sets == 1
}

var seed int64 = 2709

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	arrays, n, rounds := 20, 100000, 5
	small := []int64{2, 3, 5, 7}
	all := make([][]int64, arrays)
	for a := range all {
		all[a] = make([]int64, n)
		for i := range all[a] {
			if a%2 == 0 {
				p := small[nextRandom()%4]
				all[a][i] = p * (wide()%14285 + 1)
			} else {
				all[a][i] = wide()%99999 + 2
			}
		}
	}
	var yes, check int64
	for r := 0; r < rounds; r++ {
		for _, nums := range all {
			can := canTraverseAllPairs(nums)
			c := int64(1)
			if can {
				yes++
				c = 2
			}
			check = (check*31 + c + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d numbers up to 100000, %d rounds: %d traversable, checksum %d\n", arrays, n, rounds, yes, check)
}
