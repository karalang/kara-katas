// Benchmark: LeetCode #946 Validate Stack Sequences -- the ★ arm, the
// stack replayed, on sequences of 1000 values, LeetCode's longest.
// Mirrors validate_stack_sequences.kara, .c, .rs and .py.
package main

import "fmt"

func validateStackSequences(pushed, popped []int64) bool {
	var stack []int64
	j := 0
	for _, v := range pushed {
		stack = append(stack, v)
		for len(stack) > 0 && stack[len(stack)-1] == popped[j] {
			stack = stack[:len(stack)-1]
			j++
		}
	}
	return j == len(popped)
}

var seed int64 = 946

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const rounds, count, n = 2500, 20, 1000
	// the values 0 to 1000 in a random order, the first 1000 pushed, and
	// the pops of a random run of pushes and pops, every second one with
	// two neighbouring pops swapped
	var pushes, pops [][]int64
	for c := 0; c < count; c++ {
		all := make([]int64, 1001)
		for v := range all {
			all[v] = int64(v)
		}
		for i := 0; i < n; i++ {
			j := i + int(nextRandom()%int64(1001-i))
			all[i], all[j] = all[j], all[i]
		}
		pushed := append([]int64(nil), all[:n]...)
		var stack, popped []int64
		i := 0
		for len(popped) < n {
			if i < n && (len(stack) == 0 || nextRandom()%2 == 0) {
				stack = append(stack, pushed[i])
				i++
			} else {
				popped = append(popped, stack[len(stack)-1])
				stack = stack[:len(stack)-1]
			}
		}
		if c%2 == 1 {
			k := int(nextRandom() % (n - 1))
			popped[k], popped[k+1] = popped[k+1], popped[k]
		}
		pushes = append(pushes, pushed)
		pops = append(pops, popped)
	}
	var fits, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			k := (r + i) % count
			ok := validateStackSequences(pushes[k], pops[k])
			if ok {
				fits++
			}
			add := int64(2)
			if ok {
				add = 1
			}
			check = (check*31 + add) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d pairs of sequences of %d values: %d fit, checksum %d\n", rounds, count, n, fits, check)
}
