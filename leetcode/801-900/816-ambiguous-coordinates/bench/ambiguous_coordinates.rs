// Benchmark for #816: Ambiguous Coordinates -- mirror of the ★ arm (every
// split and every point), with the same workload as
// ambiguous_coordinates.kara.

fn ambiguous_coordinates(s: &str) -> Vec<String> {
    let digits = &s[1..s.len() - 1];
    let mut out: Vec<String> = Vec::new();
    for cut in 1..digits.len() {
        let lefts = numbers(&digits[..cut]);
        let rights = numbers(&digits[cut..]);
        for x in &lefts {
            for y in &rights {
                out.push(format!("({}, {})", x, y));
            }
        }
    }
    out
}

fn numbers(part: &str) -> Vec<String> {
    let mut found: Vec<String> = Vec::new();
    for point in 1..part.len() + 1 {
        let whole = &part[..point];
        let fraction = &part[point..];
        if (whole == "0" || !whole.starts_with('0')) && !fraction.ends_with('0') {
            if fraction.is_empty() {
                found.push(whole.to_string());
            } else {
                found.push(format!("{}.{}", whole, fraction));
            }
        }
    }
    found
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64;
    let rounds: i64 = 400000;
    let mut seed: i64 = 816;
    let mut strings: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut digits: Vec<i64> = Vec::new();
        for _ in 0..10 {
            digits.push(if next_random(&mut seed) % 4 == 0 {
                0
            } else {
                next_random(&mut seed) % 10
            });
        }
        strings.push(digits);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let g = (round % count as i64) as usize;
        let at = (next_random(&mut seed) % 10) as usize;
        strings[g][at] = if next_random(&mut seed) % 4 == 0 {
            0
        } else {
            next_random(&mut seed) % 10
        };
        let mut s = "(".to_string();
        for d in &strings[g] {
            s.push_str(&format!("{}", d));
        }
        s.push(')');
        let answer = ambiguous_coordinates(&s);
        total += answer.len() as i64;
        for c in &answer {
            checksum = (checksum * 131 + c.len() as i64) % 1000000007;
        }
    }
    println!(
        "{} rounds of 10 digits: {} coordinates, checksum {}",
        rounds, total, checksum
    );
}
