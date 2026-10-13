// Benchmark for #537: the ★ arm (split, then the schoolbook product);
// see ../README.md § Benchmarks. Mirrors complex_number_multiply.kara.

fn parts(num: &str) -> (i64, i64) {
    let halves: Vec<&str> = num.split('+').collect();
    let re: i64 = halves[0].parse().unwrap();
    let im: i64 = halves[1][..halves[1].len() - 1].parse().unwrap();
    (re, im)
}

fn complex_number_multiply(num1: &str, num2: &str) -> String {
    let (a, b) = parts(num1);
    let (c, d) = parts(num2);
    format!("{}+{}i", a * c - b * d, a * d + b * c)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 537;
    let mut nums: Vec<String> = Vec::new();
    for _ in 0..2000 {
        let re = next_random(&mut seed) % 201 - 100;
        let im = next_random(&mut seed) % 201 - 100;
        nums.push(format!("{}+{}i", re, im));
    }
    let n = nums.len();
    let rounds = 2500;
    let mut real: i64 = 0;
    let mut length: i64 = 0;
    for r in 0..rounds {
        for i in 0..n {
            let p = complex_number_multiply(&nums[i], &nums[(i * 7 + r) % n]);
            if p.ends_with("+0i") {
                real += 1;
            }
            length += p.len() as i64;
        }
    }
    println!("{} numbers, {} rounds: {} real, length {}", n, rounds, real, length);
}
