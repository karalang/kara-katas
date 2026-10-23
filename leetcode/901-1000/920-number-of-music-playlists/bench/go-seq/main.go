// LeetCode #920: Number of Music Playlists -- bench: a table over the
// length and the distinct songs so far. Mirrors num_music_playlists.kara.
package main

import "fmt"

func numMusicPlaylists(n, goal, k int64) int64 {
	const modulus = 1000000007
	dp := make([][]int64, goal+1)
	for i := range dp {
		dp[i] = make([]int64, n+1)
	}
	dp[0][0] = 1
	for i := int64(1); i <= goal; i++ {
		for j := int64(1); j <= min(i, n); j++ {
			fresh := dp[i-1][j-1] * (n - j + 1) % modulus
			var again int64
			if j > k {
				again = dp[i-1][j] * (j - k) % modulus
			}
			dp[i][j] = (fresh + again) % modulus
		}
	}
	return dp[goal][n]
}

func main() {
	const top = 64
	var count, sum, check int64
	for goal := int64(1); goal <= top; goal++ {
		for n := int64(1); n <= goal; n++ {
			for k := int64(0); k < n; k++ {
				r := numMusicPlaylists(n, goal, k)
				count++
				sum += r
				check = (check*1000003 + r) % 1000000007
			}
		}
	}
	fmt.Printf("every case with goal up to %d: %d cases, answers summing to %d, checksum %d\n", top, count, sum, check)
}
