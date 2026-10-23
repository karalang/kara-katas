// LeetCode #920: Number of Music Playlists -- bench: a table over the
// length and the distinct songs so far. Mirrors num_music_playlists.kara.

fn num_music_playlists(n: i64, goal: i64, k: i64) -> i64 {
    let modulus = 1000000007;
    let (n, goal) = (n as usize, goal as usize);
    let mut dp = vec![vec![0i64; n + 1]; goal + 1];
    dp[0][0] = 1;
    for i in 1..=goal {
        for j in 1..=i.min(n) {
            let fresh = dp[i - 1][j - 1] * (n - j + 1) as i64 % modulus;
            let again = if j as i64 > k { dp[i - 1][j] * (j as i64 - k) % modulus } else { 0 };
            dp[i][j] = (fresh + again) % modulus;
        }
    }
    dp[goal][n]
}

fn main() {
    let top = 64;
    let mut count = 0;
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for goal in 1..=top {
        for n in 1..=goal {
            for k in 0..n {
                let r = num_music_playlists(n, goal, k);
                count += 1;
                sum += r;
                check = (check * 1000003 + r) % 1000000007;
            }
        }
    }
    println!("every case with goal up to {top}: {count} cases, answers summing to {sum}, checksum {check}");
}
