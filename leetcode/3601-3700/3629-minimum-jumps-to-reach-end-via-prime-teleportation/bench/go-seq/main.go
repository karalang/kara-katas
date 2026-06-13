// LeetCode #3629 — Go seq bench peer for bfs_sieve.kara. Same algorithm,
// same workload, same sink as the Kara/Rust/C mirrors.

package main

import "fmt"

func buildFactors(cap int64) [][]int64 {
	factors := make([][]int64, cap+1)
	for i := int64(2); i <= cap; i++ {
		if len(factors[i]) == 0 {
			for j := i; j <= cap; j += i {
				factors[j] = append(factors[j], i)
			}
		}
	}
	return factors
}

func minJumps(nums []int64) int64 {
	n := int64(len(nums))
	if n <= 1 {
		return 0
	}

	cap := int64(1)
	for _, v := range nums {
		if v > cap {
			cap = v
		}
	}
	factors := buildFactors(cap)

	bucket := make(map[int64][]int64)
	for j, v := range nums {
		if v >= 2 {
			for _, p := range factors[v] {
				bucket[p] = append(bucket[p], int64(j))
			}
		}
	}

	visited := make([]bool, n)
	visited[0] = true

	type node struct {
		i, d int64
	}
	queue := []node{{0, 0}}
	head := 0

	for head < len(queue) {
		cur := queue[head]
		head++
		i, d := cur.i, cur.d
		if i == n-1 {
			return d
		}
		if i > 0 && !visited[i-1] {
			visited[i-1] = true
			queue = append(queue, node{i - 1, d + 1})
		}
		if i+1 < n && !visited[i+1] {
			visited[i+1] = true
			queue = append(queue, node{i + 1, d + 1})
		}
		v := nums[i]
		if v >= 2 && factors[v][0] == v {
			if indices, ok := bucket[v]; ok {
				delete(bucket, v)
				for _, j := range indices {
					if !visited[j] {
						visited[j] = true
						queue = append(queue, node{j, d + 1})
					}
				}
			}
		}
	}
	return -1
}

func main() {
	const n = 50000
	data := make([]int64, n)
	for i := int64(0); i < n; i++ {
		data[i] = (i*7919+13)%999983 + 2
	}

	var sum int64
	for k := 0; k < 50; k++ {
		sum += minJumps(data)
	}
	fmt.Println(sum)
}
