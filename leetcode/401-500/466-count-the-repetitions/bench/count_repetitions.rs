// Benchmark for #466: mirror of count_repetitions.kara (the ★ arm: find
// the cycle) on the same workload. The memo of positions is a HashMap,
// like the Kāra arm's Map.
use std::collections::HashMap;

fn get_max_repetitions(s1: &str, n1: i64, s2: &str, n2: i64) -> i64 {
    let a: Vec<char> = s1.chars().collect();
    let b: Vec<char> = s2.chars().collect();
    let mut index = 0;
    let mut count = 0;
    let mut seen: HashMap<usize, (i64, i64)> = HashMap::new();
    let mut k = 0;
    while k < n1 {
        for &c in &a {
            if c == b[index] {
                index += 1;
                if index == b.len() {
                    index = 0;
                    count += 1;
                }
            }
        }
        k += 1;
        if let Some(&(k0, count0)) = seen.get(&index) {
            let cycle = k - k0;
            let cycles = (n1 - k) / cycle;
            count += cycles * (count - count0);
            k += cycles * cycle;
            while k < n1 {
                for &c in &a {
                    if c == b[index] {
                        index += 1;
                        if index == b.len() {
                            index = 0;
                            count += 1;
                        }
                    }
                }
                k += 1;
            }
            break;
        }
        seen.insert(index, (k, count));
    }
    count / n2
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let pairs = 100;
    let rounds = 1000;
    let mut seed: i64 = 466;
    let mut firsts: Vec<String> = Vec::new();
    let mut seconds: Vec<String> = Vec::new();
    for _ in 0..pairs {
        let mut s1 = String::new();
        let mut letters: Vec<char> = Vec::new();
        for _ in 0..100 {
            let c = char::from_u32(97 + (next_random(&mut seed) % 26) as u32).unwrap();
            s1.push(c);
            letters.push(c);
        }
        let mut s2 = String::new();
        for _ in 0..1 + next_random(&mut seed) % 100 {
            s2.push(letters[(next_random(&mut seed) % 100) as usize]);
        }
        firsts.push(s1);
        seconds.push(s2);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        for p in 0..pairs {
            let n1 = 1 + (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000000;
            let n2 = 1 + next_random(&mut seed) % 100;
            let m = get_max_repetitions(&firsts[p], n1, &seconds[p], n2);
            total += m;
            checksum = (checksum * 31 + m) % 1000000007;
        }
    }
    println!("{} rounds on {} pairs: {} repetitions in all, checksum {}", rounds, pairs, total, checksum);
}
