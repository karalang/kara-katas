// Benchmark for #459: mirror of repeated_substring.kara (the ★ arm, every
// proper divisor) on the same workload.

fn repeated_substring_pattern(s: &str) -> bool {
    let cs: Vec<char> = s.chars().collect();
    let n = cs.len();
    for d in 1..n / 2 + 1 {
        if n % d != 0 {
            continue;
        }
        let mut repeats = true;
        for i in d..n {
            if cs[i] != cs[i - d] {
                repeats = false;
                break;
            }
        }
        if repeats {
            return true;
        }
    }
    false
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let strings = 10;
    let n: i64 = 100000;
    let rounds = 40;
    let units: [i64; 10] = [1, 5, 32, 100, 625, 1000, 3125, 5000, 20000, 50000];
    let mut seed: i64 = 459;
    let mut all: Vec<String> = Vec::new();
    for a in 0..strings {
        let mut unit = String::new();
        for _ in 0..units[a] {
            unit.push(char::from_u32(97 + (next_random(&mut seed) % 26) as u32).unwrap());
        }
        all.push(unit.repeat((n / units[a]) as usize));
    }
    let mut found = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        for a in 0..strings {
            let k = n / 2 + (next_random(&mut seed) * 65536 + next_random(&mut seed)) % (n / 2);
            let punch = next_random(&mut seed) % 2 == 0;
            let original = all[a].clone();
            if punch {
                let mut cs: Vec<char> = all[a].chars().collect();
                let c = cs[k as usize] as u32;
                cs[k as usize] = char::from_u32(97 + (c - 97 + 1) % 26).unwrap();
                all[a] = cs.iter().collect();
            }
            let has = repeated_substring_pattern(&all[a]);
            all[a] = original;
            if has {
                found += 1;
            }
            checksum = (checksum * 31 + if has { units[a] } else { k }) % 1000000007;
        }
    }
    println!("{} rounds on {} strings of {}: {} repeat a substring, checksum {}", rounds, strings, n, found, checksum);
}
