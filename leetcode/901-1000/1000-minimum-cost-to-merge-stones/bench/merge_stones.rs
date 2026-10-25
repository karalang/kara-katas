// Benchmark: LeetCode #1000 Minimum Cost to Merge Stones -- the ★ arm,
// an interval table by length, on rows of up to 30 piles, LeetCode's
// largest. Mirrors merge_stones.kara, .c, .py and go-seq/.

fn merge_stones(stones: &[i64], k: i64) -> i64 {
    let n = stones.len();
    let k = k as usize;
    if (n - 1) % (k - 1) != 0 {
        return -1;
    }
    let mut prefix = vec![0i64; n + 1];
    for i in 0..n {
        prefix[i + 1] = prefix[i] + stones[i];
    }
    let mut dp = vec![vec![0i64; n]; n];
    for length in k..n + 1 {
        for i in 0..n - length + 1 {
            let j = i + length - 1;
            let mut best: i64 = 1 << 60;
            let mut m = i;
            while m < j {
                best = best.min(dp[i][m] + dp[m + 1][j]);
                m += k - 1;
            }
            if (length - 1) % (k - 1) == 0 {
                best += prefix[j + 1] - prefix[i];
            }
            dp[i][j] = best;
        }
    }
    dp[0][n - 1]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds: i64 = 5000;
    let mut seed = 1000;
    // 20 rows, k from 2 to 11 twice over, each with as many piles of 1 to
    // 100 stones, up to 30, as k can merge down to one pile
    let mut rows: Vec<Vec<i64>> = Vec::new();
    let mut ks: Vec<i64> = Vec::new();
    for t in 0..20 {
        let k = 2 + t % 10;
        let n = 1 + 29 / (k - 1) * (k - 1);
        rows.push((0..n).map(|_| 1 + next_random(&mut seed) % 100).collect());
        ks.push(k);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..20 {
            let t = ((r + i) % 20) as usize;
            let got = merge_stones(&rows[t], ks[t]);
            total += got;
            check = (check * 31 + got + 2) % 1000000007;
        }
    }
    println!("{} rounds over 20 rows of up to 30 piles: cost {}, checksum {}", rounds, total, check);
}
