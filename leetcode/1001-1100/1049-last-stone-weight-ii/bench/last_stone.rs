// LeetCode #1049: Last Stone Weight II -- Rust mirror of
// bench/last_stone.kara.

fn last_stone_weight_ii(stones: &[i64]) -> i64 {
    let total: i64 = stones.iter().sum();
    let half = total / 2;
    let mut made = vec![false; (half + 1) as usize];
    made[0] = true;
    for &s in stones {
        let mut t = half;
        while t >= s {
            if made[(t - s) as usize] {
                made[t as usize] = true;
            }
            t -= 1;
        }
    }
    let mut best = half;
    while !made[best as usize] {
        best -= 1;
    }
    total - 2 * best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let (lists, count, rounds) = (1000, 30, 10);
    let mut seed = 1049;
    let mut all: Vec<Vec<i64>> = Vec::new();
    for _ in 0..lists {
        let mut stones = Vec::new();
        for _ in 0..count {
            stones.push(next_random(&mut seed) % 100 + 1);
        }
        all.push(stones);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..rounds {
        for stones in &all {
            let answer = last_stone_weight_ii(stones);
            total += answer;
            check = (check * 131 + answer) % 1000000007;
        }
    }
    println!("{lists} lists of {count} stones, {rounds} rounds: total {total}, checksum {check}");
}
