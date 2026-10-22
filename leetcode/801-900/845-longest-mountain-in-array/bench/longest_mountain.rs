// Benchmark for #845: Longest Mountain in Array -- Rust twin of the Kāra ★
// arm (one pass with two counters).

fn longest_mountain(arr: &[i64]) -> i64 {
    let mut best = 0;
    let mut up = 0;
    let mut down = 0;
    for i in 1..arr.len() {
        if (down > 0 && arr[i - 1] < arr[i]) || arr[i - 1] == arr[i] {
            up = 0;
            down = 0;
        }
        if arr[i - 1] < arr[i] {
            up += 1;
        } else if arr[i - 1] > arr[i] {
            down += 1;
        }
        if up > 0 && down > 0 {
            best = best.max(up + down + 1);
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64usize;
    let rounds = 20000usize;
    let n = 10000usize;
    let mut seed: i64 = 845;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for g in 0..count {
        let mut arr: Vec<i64> = Vec::new();
        if g % 3 == 0 {
            for _ in 0..n {
                arr.push(next_random(&mut seed) % 10001);
            }
        } else if g % 3 == 1 {
            let mut v = 5000;
            for _ in 0..n {
                arr.push(v);
                v += next_random(&mut seed) % 3 - 1;
            }
        } else {
            while arr.len() < n {
                let up = next_random(&mut seed) % 40;
                let down = next_random(&mut seed) % 40;
                let base = next_random(&mut seed) % 100;
                for k in 0..up + 1 {
                    if arr.len() < n {
                        arr.push(base + k);
                    }
                }
                for k in 0..down {
                    if arr.len() < n {
                        arr.push(base + up - k - 1);
                    }
                }
            }
        }
        arrays.push(arr);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let m = longest_mountain(&arrays[round % count]);
        total += m;
        checksum = (checksum * 31 + m) % 1000000007;
    }
    println!("{rounds} rounds of {count} arrays: lengths sum to {total}, checksum {checksum}");
}
