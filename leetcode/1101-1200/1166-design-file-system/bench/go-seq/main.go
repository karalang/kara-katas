// LeetCode #1166: Design File System -- the ★ arm's bench in Go: one map
// from a made path to its value.
package main

import (
	"fmt"
	"strings"
)

type FileSystem struct {
	paths map[string]int64
}

func NewFileSystem() FileSystem {
	return FileSystem{paths: map[string]int64{}}
}

func (fs *FileSystem) CreatePath(path string, value int64) bool {
	if len(path) == 0 || path == "/" {
		return false
	}
	if _, ok := fs.paths[path]; ok {
		return false
	}
	parent := path[:strings.LastIndex(path, "/")]
	if len(parent) > 0 {
		if _, ok := fs.paths[parent]; !ok {
			return false
		}
	}
	fs.paths[path] = value
	return true
}

func (fs *FileSystem) Get(path string) int64 {
	if v, ok := fs.paths[path]; ok {
		return v
	}
	return -1
}

var seed int64 = 1166

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	names := []string{"a", "b", "ab", "le", "leet", "code"}
	paths := make([][]string, 16)
	creates := make([][]bool, 16)
	for k := 0; k < 16; k++ {
		for i := 0; i < 10000; i++ {
			parts := 1 + nextRandom()%5
			p := ""
			for j := int64(0); j < parts; j++ {
				p = p + "/" + names[nextRandom()%6]
			}
			paths[k] = append(paths[k], p)
			creates[k] = append(creates[k], nextRandom()%4 != 0)
		}
	}
	var made, check int64
	for r := 0; r < 100; r++ {
		for k := 0; k < 16; k++ {
			from := nextRandom() % 5000
			fs := NewFileSystem()
			for i := from; i < 10000; i++ {
				var a int64
				if creates[k][i] {
					if fs.CreatePath(paths[k][i], i) {
						a = 1
					}
					made += a
				} else {
					a = fs.Get(paths[k][i])
				}
				check = (check*31 + a + 2) % 1000000007
			}
		}
	}
	fmt.Printf("100 rounds over 16 lists of 10^4 operations: made %d, checksum %d\n", made, check)
}
