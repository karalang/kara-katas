// LeetCode #1690: Stone Game VII -- the bench's Rust mirror: the ★ arm on
// 40 random rows of 1000 stones, all drawn first, each answered 4 times.

fn stone_game(stones: &[i32]) -> i32 {
    let n = stones.len();
    let mut prefix = vec![0i32; n + 1];
    for i in 0..n {
        prefix[i + 1] = prefix[i] + stones[i];
    }
    let mut best = vec![0i32; n];
    for i in (0..n).rev() {
        for j in i + 1..n {
            let take_left = prefix[j + 1] - prefix[i + 1] - best[j];
            let take_right = prefix[j] - prefix[i] - best[j - 1];
            best[j] = take_left.max(take_right);
        }
    }
    best[n - 1]
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 40;
    let size = 1000;
    let rounds = 4;
    let mut seed = 1690;
    let mut rows: Vec<Vec<i32>> = Vec::new();
    for _ in 0..count {
        rows.push((0..size).map(|_| (next_random(&mut seed) % 1000 + 1) as i32).collect());
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for stones in rows.iter() {
            let answer = stone_game(stones) as i64;
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{count} rows of {size} stones, {rounds} rounds: answers sum to {total}, checksum {check}");
}
