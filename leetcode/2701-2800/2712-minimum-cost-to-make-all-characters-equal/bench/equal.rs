// LeetCode #2712: Minimum Cost to Make All Characters Equal -- the bench
// (equal.kara in Rust): each boundary between unequal neighbours priced
// at the cheaper flip across it.

fn minimum_cost(s: &str) -> i64 {
    let bits = s.as_bytes();
    let n = bits.len() as i64;
    let mut cost: i64 = 0;
    for i in 1..n {
        if bits[i as usize] != bits[(i - 1) as usize] {
            cost += i.min(n - i);
        }
    }
    cost
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100;
    let rounds = 5;
    let mut seed: i64 = 2712;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..count {
        let change = next_random(&mut seed) % 9;
        let mut bits = String::new();
        let mut last = '0';
        for _ in 0..100000 {
            if next_random(&mut seed) % 8 < change {
                last = if last == '0' { '1' } else { '0' };
            }
            bits.push(last);
        }
        strings.push(bits);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for s in strings.iter() {
            let cost = minimum_cost(s);
            sum += cost;
            check = (check * 31 + cost + r) % 1000000007;
        }
    }
    println!("{} strings of 100000 bits, {} rounds: costs sum to {}, checksum {}", count, rounds, sum, check);
}
