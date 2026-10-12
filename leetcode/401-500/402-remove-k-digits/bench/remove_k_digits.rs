// Benchmark for #402: mirror of remove_k_digits.kara (a stack that keeps
// digits rising).

fn remove_kdigits(num: &str, k: i64) -> String {
    let mut left = k;
    let mut stack: Vec<u8> = Vec::new();
    for c in num.bytes() {
        while left > 0 && !stack.is_empty() && stack[stack.len() - 1] > c {
            stack.pop();
            left -= 1;
        }
        stack.push(c);
    }
    while left > 0 {
        stack.pop();
        left -= 1;
    }
    let mut out = String::new();
    for c in stack.iter() {
        if out.is_empty() && *c == 48 {
            continue;
        }
        out.push(*c as char);
    }
    if out.is_empty() {
        out.push('0');
    }
    out
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let numbers = 300;
    let n: i64 = 100000;
    let mut seed: i64 = 402;
    let mut kept: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..numbers {
        let mut num = String::new();
        num.push((49 + step(&mut seed) % 9) as u8 as char);
        for _ in 1..n {
            num.push((48 + step(&mut seed) % 10) as u8 as char);
        }
        let k = step(&mut seed) % (n + 1);
        let r = remove_kdigits(&num, k);
        kept += r.len() as i64;
        for b in r.bytes() {
            checksum = (checksum * 31 + b as i64) % 1000000007;
        }
    }
    println!("{} numbers of {} digits: {} digits kept, checksum {}", numbers, n, kept, checksum);
}
