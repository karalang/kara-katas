// Benchmark for #422: mirror of valid_word_square.kara (every cell
// against its mirror). A flip rebuilds the row, as the Kāra program does.
package main

import (
	"fmt"
	"os"
	"strconv"
)

func validWordSquare(words []string) bool {
	n := len(words)
	for i := 0; i < n; i++ {
		row := words[i]
		for j := 0; j < len(row); j++ {
			if j >= n {
				return false
			}
			mirror := words[j]
			if i >= len(mirror) || mirror[i] != row[j] {
				return false
			}
		}
	}
	return true
}

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func flip(words []string, i, j int64) {
	bytes := words[i]
	word := make([]byte, len(bytes))
	for k := 0; k < len(bytes); k++ {
		if int64(k) == j {
			word[k] = 195 - bytes[k]
		} else {
			word[k] = bytes[k]
		}
	}
	words[i] = string(word)
}

func main() {
	rounds := int64(6000)
	if len(os.Args) > 1 {
		rounds, _ = strconv.ParseInt(os.Args[1], 10, 64)
	}
	n := int64(500)
	seed := int64(422)
	grid := make([]int64, n*n)
	for i := int64(0); i < n; i++ {
		for j := i; j < n; j++ {
			c := step(&seed) % 2
			grid[i*n+j] = c
			grid[j*n+i] = c
		}
	}
	lengths := []int64{n}
	for i := int64(1); i < n; i++ {
		drop := int64(0)
		if step(&seed)%4 == 0 {
			drop = 1
		}
		lengths = append(lengths, max(1, lengths[i-1]-drop))
	}
	words := make([]string, 0, n)
	cells := 0
	for i := int64(0); i < n; i++ {
		height := int64(0)
		for height < n && lengths[height] > i {
			height++
		}
		word := make([]byte, 0)
		for j := int64(0); j < min(lengths[i], height); j++ {
			word = append(word, byte(97+grid[i*n+j]))
		}
		words = append(words, string(word))
		cells += len(word)
	}
	var valid, checksum int64
	for r := int64(0); r < rounds; r++ {
		i := step(&seed) % n
		j := step(&seed) % int64(len(words[i]))
		flip(words, i, j)
		if r%3 != 0 {
			flip(words, j, i)
		}
		answer := validWordSquare(words)
		add := int64(0)
		if answer {
			valid++
			add = r + 1
		}
		checksum = (checksum*31 + add) % 1000000007
		if r%3 == 0 {
			flip(words, i, j)
		}
	}
	fmt.Printf("%d rounds on %d words, %d letters: %d valid, checksum %d\n", rounds, n, cells, valid, checksum)
}
