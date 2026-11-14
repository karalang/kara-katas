// LeetCode #1531: String Compression II -- bench: the ★ arm over 300
// random strings of 1 to 100 letters, each over its own 1 to 4 letters with
// k from 0 to its length, built once and answered 10 times.

fn run_length(count: i64) -> i64 {
    if count == 1 {
        1
    } else if count < 10 {
        2
    } else if count < 100 {
        3
    } else {
        4
    }
}

fn get_length_of_optimal_compression(s: &str, k: i64) -> i64 {
    let b = s.as_bytes();
    let n = b.len();
    let k = k as usize;
    let mut best = vec![vec![0i64; k + 1]; n + 1];
    for i in (0..n).rev() {
        for j in 0..k + 1 {
            let mut shortest = n as i64 + 1;
            if j > 0 {
                shortest = best[i + 1][j - 1];
            }
            let mut same = 0;
            let mut other = 0;
            for end in i..n {
                if b[end] == b[i] {
                    same += 1;
                } else {
                    other += 1;
                }
                if other > j {
                    break;
                }
                shortest = shortest.min(run_length(same) + best[end + 1][j - other]);
            }
            best[i][j] = shortest;
        }
    }
    best[0][k]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1531;
    let mut cases: Vec<(String, i64)> = Vec::new();
    for _ in 0..300 {
        let n = next_random(&mut seed) % 100 + 1;
        let over = next_random(&mut seed) % 4 + 1;
        let mut s = String::new();
        for _ in 0..n {
            s.push((97 + next_random(&mut seed) % over) as u8 as char);
        }
        let k = next_random(&mut seed) % (n + 1);
        cases.push((s, k));
    }
    let mut check = 0;
    for _ in 0..10 {
        for (s, k) in cases.iter() {
            check = mix(check, get_length_of_optimal_compression(s, *k));
        }
    }
    println!("10 passes over 300 strings of up to 100 letters: checksum {}", check);
}
