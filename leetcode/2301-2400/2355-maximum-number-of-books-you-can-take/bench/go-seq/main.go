// LeetCode #2355: Maximum Number of Books You Can Take -- the bench, the ★
// arm in Go: the most books from a run ending at each shelf, from the
// nearest shelf to the left that caps the run, found on a monotonic stack.
package main

import "fmt"

func maximumBooks(books []int64) int64 {
	n := int64(len(books))
	best := make([]int64, n)
	stack := make([]int64, 0)
	answer := int64(0)
	for i := int64(0); i < n; i++ {
		for len(stack) > 0 && books[stack[len(stack)-1]]-stack[len(stack)-1] >= books[i]-i {
			stack = stack[:len(stack)-1]
		}
		if len(stack) > 0 {
			j := stack[len(stack)-1]
			length := i - j
			best[i] = length*books[i] - length*(length-1)/2 + best[j]
		} else {
			length := i + 1
			if books[i] < length {
				length = books[i]
			}
			best[i] = length*books[i] - length*(length-1)/2
		}
		stack = append(stack, i)
		if best[i] > answer {
			answer = best[i]
		}
	}
	return answer
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// array a holds 10^5 shelves: up to 10^5 books every (a + 2)^2-th
	// shelf, up to 100 (a + 1) between
	seed := int64(2355)
	arrays := make([][]int64, 0, 10)
	for a := int64(0); a < 10; a++ {
		books := make([]int64, 0, 100000)
		for i := int64(0); i < 100000; i++ {
			r := nextRandom(&seed)
			if i%((a+2)*(a+2)) == 0 {
				books = append(books, r*3%100001)
			} else {
				books = append(books, r%(100*(a+1)+1))
			}
		}
		arrays = append(arrays, books)
	}
	check := int64(0)
	for p := int64(0); p < 50; p++ {
		for _, books := range arrays {
			check = (check*31 + maximumBooks(books)%1000000007 + p) % 1000000007
		}
	}
	fmt.Printf("50 passes over 10 arrays of 10^5 shelves: checksum %d\n", check)
}
