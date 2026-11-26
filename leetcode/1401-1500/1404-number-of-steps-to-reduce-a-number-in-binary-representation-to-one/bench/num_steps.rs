// LeetCode #1404 bench, Rust: the same walk with a carry, workload and
// checksum as num_steps.kara.

fn num_steps(s: &String) -> i32 {
    let bits: Vec<char> = s.chars().collect();
    let mut steps: i32 = 0;
    let mut carry: i32 = 0;
    for i in (1..bits.len()).rev() {
        let bit = if bits[i] == '1' { 1 } else { 0 } + carry;
        if bit == 1 {
            steps += 2;
            carry = 1;
        } else {
            steps += 1;
        }
    }
    steps + carry
}

fn main() {
    let mut seed: i64 = 1404;
    let mut pool = String::new();
    for _ in 0..100000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        pool.push(if seed / 65536 % 2 == 0 { '0' } else { '1' });
    }
    let mut check: i64 = 0;
    for r in 0..200000i64 {
        let at = ((check + r * 7919) % 99501) as usize;
        let s = "1".to_string() + &pool[at..at + 499];
        check = (check * 131 + num_steps(&s) as i64) % 1000000007;
    }
    println!("200000 numbers of 500 digits: checksum {}", check);
}
