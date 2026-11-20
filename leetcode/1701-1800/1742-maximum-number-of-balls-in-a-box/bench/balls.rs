// LeetCode #1742: Maximum Number of Balls in a Box -- the bench
// (balls.kara in Rust): a count for every digit sum.

fn count_balls(low_limit: i32, high_limit: i32) -> i32 {
    let mut boxes = [0i32; 46];
    for ball in low_limit..high_limit + 1 {
        let mut rest = ball;
        let mut sum = 0;
        while rest > 0 {
            sum += rest % 10;
            rest /= 10;
        }
        boxes[sum as usize] += 1;
    }
    *boxes.iter().max().unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let count = 200;
    let rounds: i64 = 20;
    let mut seed: i64 = 1742;
    let mut ranges: Vec<(i32, i32)> = Vec::new();
    for _ in 0..count {
        let a = wide(&mut seed) % 100000 + 1;
        let b = wide(&mut seed) % 100000 + 1;
        ranges.push((a.min(b) as i32, a.max(b) as i32));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for &(low, high) in ranges.iter() {
            let answer = count_balls(low, high) as i64;
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{} ranges inside 1 to 100000, {} rounds: largest boxes sum to {}, checksum {}", count, rounds, sum, check);
}
