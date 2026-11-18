// LeetCode #2279: Maximum Bags With Full Capacity of Rocks -- the bench,
// the ★ arm.

fn maximum_bags(capacity: &[i64], rocks: &[i64], additional_rocks: i64) -> i64 {
    let mut lack: Vec<i64> = Vec::new();
    for i in 0..capacity.len() {
        lack.push(capacity[i] - rocks[i]);
    }
    lack.sort();
    let mut left = additional_rocks;
    let mut full = 0;
    for &need in &lack {
        if need > left {
            break;
        }
        left -= need;
        full += 1;
    }
    full
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn draw(seed: &mut i64, high: i64) -> i64 {
    let top = next_random(seed);
    (top * 32768 + next_random(seed)) % high
}

fn main() {
    let mut seed = 2279;
    let mut check = 0;
    for _ in 0..50 {
        let mut capacity: Vec<i64> = Vec::new();
        let mut rocks: Vec<i64> = Vec::new();
        for _ in 0..50000 {
            let c = draw(&mut seed, 1000000000) + 1;
            capacity.push(c);
            rocks.push(draw(&mut seed, c + 1));
        }
        let spare = draw(&mut seed, 1000000000) + 1;
        check = (check * 31 + maximum_bags(&capacity, &rocks, spare)) % 1000000007;
    }
    println!("50 sets of 5 * 10^4: checksum {check}");
}
