// LeetCode #2048 -- the ★ arm as a benchmark; mirror of beautiful.kara.

fn is_balanced(x: i64) -> bool {
    let mut counts = [0i64; 10];
    let mut y = x;
    while y > 0 {
        counts[(y % 10) as usize] += 1;
        y /= 10;
    }
    for d in 0..10 {
        if counts[d] != 0 && counts[d] != d as i64 {
            return false;
        }
    }
    true
}

fn next_beautiful_number(n: i64) -> i64 {
    let mut x = n + 1;
    while !is_balanced(x) {
        x += 1;
    }
    x
}

fn main() {
    let (mut calls, mut sum, mut check) = (0i64, 0i64, 0i64);
    for k in 0..1000i64 {
        let x = next_beautiful_number(k * 1000 + k * 7 % 1000);
        calls += 1;
        sum += x;
        check = (check * 31 + x) % 1_000_000_007;
    }
    println!("{} calls: sum {}, checksum {}", calls, sum, check);
}
