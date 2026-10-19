// LeetCode 769 — Max Chunks To Make Sorted: benchmark, the ★ arm in Rust.
// Sixty-four near-sorted permutations of 2,000, built once; 150,000
// rounds each count the next one's chunks.

fn max_chunks_to_sorted(arr: &[i64]) -> i64 {
    let mut chunks = 0;
    let mut largest = 0;
    for (i, &x) in arr.iter().enumerate() {
        largest = largest.max(x);
        if largest == i as i64 {
            chunks += 1;
        }
    }
    chunks
}

fn main() {
    let mut seed: i64 = 769;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let rounds: i64 = 150000;
    let n: i64 = 2000;
    let mut pool: Vec<Vec<i64>> = Vec::new();
    for _ in 0..64 {
        let mut arr: Vec<i64> = (0..n).collect();
        let swaps = next_random() % n;
        for _ in 0..swaps {
            let i = next_random() % n;
            let j = (i + 1 + next_random() % 4).min(n - 1);
            arr.swap(i as usize, j as usize);
        }
        pool.push(arr);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..rounds {
        let chunks = max_chunks_to_sorted(&pool[(round % 64) as usize]);
        total += chunks;
        check = (check * 31 + chunks) % 1000000007;
    }
    println!("{} permutations of 2000: {} chunks in all, checksum {}", rounds, total, check);
}
