// LeetCode 768 — Max Chunks To Make Sorted II: benchmark, the ★ arm in Rust.
// Sixty-four random arrays of 2,000 values, built once; 40,000 rounds
// each count the next one's chunks.

fn max_chunks_to_sorted(arr: &[i64]) -> i64 {
    let mut maxima: Vec<i64> = Vec::new();
    for &x in arr {
        match maxima.last() {
            Some(&top) if x < top => {
                while let Some(&t) = maxima.last() {
                    if t > x {
                        maxima.pop();
                    } else {
                        break;
                    }
                }
                maxima.push(top);
            }
            _ => maxima.push(x),
        }
    }
    maxima.len() as i64
}

fn main() {
    let mut seed: i64 = 768;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let rounds: i64 = 40000;
    let mut pool: Vec<Vec<i64>> = Vec::new();
    for _ in 0..64 {
        let noise = 1 + next_random() % 40;
        let arr: Vec<i64> = (0..2000).map(|i| i * 50 + next_random() % noise * 50).collect();
        pool.push(arr);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..rounds {
        let chunks = max_chunks_to_sorted(&pool[(round % 64) as usize]);
        total += chunks;
        check = (check * 31 + chunks) % 1000000007;
    }
    println!("{} arrays of 2000 values: {} chunks in all, checksum {}", rounds, total, check);
}
