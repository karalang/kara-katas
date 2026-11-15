// benchmark's Rust mirror of count.kara (LeetCode #2198, the ★ arm): every
// ordered triple of the values held.

fn single_divisor_triplet(nums: &[i64]) -> i64 {
    let mut count = [0i64; 101];
    for &x in nums {
        count[x as usize] += 1;
    }
    let mut total = 0i64;
    for a in 1..101i64 {
        if count[a as usize] == 0 {
            continue;
        }
        for b in 1..101i64 {
            if count[b as usize] == 0 {
                continue;
            }
            for c in 1..101i64 {
                if count[c as usize] == 0 {
                    continue;
                }
                let sum = a + b + c;
                let by_a = sum % a == 0;
                let by_b = sum % b == 0;
                let by_c = sum % c == 0;
                if (by_a && !by_b && !by_c) || (by_b && !by_a && !by_c) || (by_c && !by_a && !by_b) {
                    let (ca, cb, cc) = (count[a as usize], count[b as usize], count[c as usize]);
                    let second = if b == a { cb - 1 } else { cb };
                    let third = cc - (if c == a { 1 } else { 0 }) - (if c == b { 1 } else { 0 });
                    total += ca * second * third;
                }
            }
        }
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2198;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..20 {
        let top = 81 + a;
        arrays.push((0..100000).map(|_| next_random(&mut seed) % top + 1).collect());
    }
    let mut check: i64 = 0;
    for _ in 0..10 {
        for nums in &arrays {
            check = (check * 31 + single_divisor_triplet(nums) % 1000000007) % 1000000007;
        }
    }
    println!("10 passes over 20 arrays: checksum {}", check);
}
