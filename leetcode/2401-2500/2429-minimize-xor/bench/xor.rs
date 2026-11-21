// LeetCode #2429: Minimize XOR -- the bench, the ★ arm: num1's set bits
// taken from the top while bits are left to place, the rest laid in its
// clear bits from the bottom.

fn minimize_xor(num1: i64, num2: i64) -> i64 {
    let mut left = num2.count_ones() as i64;
    let mut x = 0;
    for bit in (0..31).rev() {
        if left > 0 && (num1 >> bit) & 1 == 1 {
            x |= 1 << bit;
            left -= 1;
        }
    }
    for bit in 0..31 {
        if left > 0 && (x >> bit) & 1 == 0 {
            x |= 1 << bit;
            left -= 1;
        }
    }
    x
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2429;
    let mut firsts: Vec<i64> = Vec::new();
    let mut seconds: Vec<i64> = Vec::new();
    for _ in 0..100000 {
        let a = next_random(&mut seed);
        firsts.push(1 + (a * 32768 + next_random(&mut seed)) % 1000000000);
        let b = next_random(&mut seed);
        seconds.push(1 + (b * 32768 + next_random(&mut seed)) % 1000000000);
    }
    let mut check: i64 = 0;
    for p in 0..10i64 {
        for i in 0..firsts.len() {
            check = (check * 31 + minimize_xor(firsts[i], seconds[i] ^ (p + 1)) + p) % 1000000007;
        }
    }
    println!("10 passes over 10^5 pairs: checksum {}", check);
}
