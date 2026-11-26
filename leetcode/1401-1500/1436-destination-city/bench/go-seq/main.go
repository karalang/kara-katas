package main

import "fmt"

func destCity(paths [][]string) string {
	starts := make(map[string]bool, len(paths))
	for _, path := range paths {
		starts[path[0]] = true
	}
	for _, path := range paths {
		if !starts[path[1]] {
			return path[1]
		}
	}
	return ""
}

func main() {
	var seed int64 = 1436
	trips := make([][][]string, 0, 1000)
	for t := 0; t < 1000; t++ {
		cities := make([]string, 0, 101)
		for c := 0; c < 101; c++ {
			name := make([]byte, 0, 10)
			for k := 0; k < 8; k++ {
				seed = (seed*1103515245 + 12345) % 2147483648
				name = append(name, byte('a'+seed/65536%26))
			}
			name = append(name, byte('a'+c/26), byte('a'+c%26))
			cities = append(cities, string(name))
		}
		seed = (seed*1103515245 + 12345) % 2147483648
		turn := int(seed / 65536 % 100)
		paths := make([][]string, 0, 100)
		for i := 0; i < 100; i++ {
			at := (i + turn) % 100
			paths = append(paths, []string{cities[at], cities[at+1]})
		}
		trips = append(trips, paths)
	}
	var check int64 = 0
	for r := 0; r < 100; r++ {
		for _, paths := range trips {
			city := destCity(paths)
			var h int64 = 0
			for i := 0; i < len(city); i++ {
				h = (h*31 + int64(city[i])) % 1000000007
			}
			check = (check*131 + h) % 1000000007
		}
	}
	fmt.Printf("10^5 trips of 100 paths: checksum %d\n", check)
}
