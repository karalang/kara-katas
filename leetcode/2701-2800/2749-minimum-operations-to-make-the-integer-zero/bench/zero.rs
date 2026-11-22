// LeetCode #2749: Minimum Operations to Make the Integer Zero -- the
// bench (zero.kara in Rust): the least k with t = num1 - k num2 a sum of
// k powers of two, by `count_ones`.

fn make_the_integer_zero(num1: i64, num2: i64) -> i64 {
    for k in 1..=60 {
        let t = num1 - k * num2;
        if (t.count_ones() as i64) <= k && k <= t {
            return k;
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 1000000;
    let rounds = 10;
    let mut seed = 2749;
    let mut pairs: Vec<(i64, i64)> = Vec::new();
    for _ in 0..count {
        let hi = next_random(&mut seed);
        let num1 = (hi * 32768 + next_random(&mut seed)) % 1000000000 + 1;
        let hi = next_random(&mut seed);
        let size = (hi * 32768 + next_random(&mut seed)) % 1000000001;
        let num2 = if next_random(&mut seed) % 2 == 0 { size } else { -size };
        pairs.push((num1, num2));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for &(num1, num2) in pairs.iter() {
            let steps = make_the_integer_zero(num1, num2);
            sum += steps;
            check = (check * 31 + steps + 1 + r) % 1000000007;
        }
    }
    println!("{count} pairs, {rounds} rounds: steps sum to {sum}, checksum {check}");
}
