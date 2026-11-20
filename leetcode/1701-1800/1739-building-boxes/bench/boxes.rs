// LeetCode #1739: Building Boxes -- the bench (boxes.kara in Rust): the
// staircase layer by layer, then the floor a box at a time.

fn minimum_boxes(n: i32) -> i32 {
    let n = n as i64;
    let mut placed: i64 = 0;
    let mut side: i64 = 0;
    while placed + (side + 1) * (side + 2) / 2 <= n {
        side += 1;
        placed += side * (side + 1) / 2;
    }
    let mut floor = side * (side + 1) / 2;
    let mut extra: i64 = 0;
    while placed < n {
        extra += 1;
        floor += 1;
        placed += extra;
    }
    floor as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let count = 20000;
    let rounds = 15;
    let mut seed: i64 = 1739;
    let counts: Vec<i32> = (0..count).map(|_| (wide(&mut seed) % 1000000000 + 1) as i32).collect();
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for &n in counts.iter() {
            let answer = minimum_boxes(n) as i64;
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{} counts up to 1000000000, {} rounds: floors sum to {}, checksum {}", count, rounds, sum, check);
}
