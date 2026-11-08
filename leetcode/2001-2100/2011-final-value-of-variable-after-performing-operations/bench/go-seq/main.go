// LeetCode #2011: Final Value of Variable After Performing Operations -- the
// ★ arm's benchmark, a mirror of final_value.kara.
package main

import "fmt"

func finalValueAfterOperations(operations []string) int64 {
	var x int64
	for _, op := range operations {
		switch op {
		case "++X", "X++":
			x++
		case "--X", "X--":
			x--
		}
	}
	return x
}

var seed int64 = 2011

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	forms := []string{"++X", "X++", "--X", "X--"}
	lists := make([][]string, 0, 20000)
	for a := 0; a < 20000; a++ {
		up := nextRandom() % 11
		operations := make([]string, 0, 100)
		for i := 0; i < 100; i++ {
			down := int64(2)
			if nextRandom()%10 < up {
				down = 0
			}
			operations = append(operations, forms[down+nextRandom()%2])
		}
		lists = append(lists, operations)
	}
	var calls, sum, check int64
	for r := 0; r < 10; r++ {
		for _, operations := range lists {
			answer := finalValueAfterOperations(operations)
			calls++
			sum += answer
			check = (check*31 + answer + 100) % 1000000007
		}
	}
	fmt.Printf("%d calls: sum %d, checksum %d\n", calls, sum, check)
}
