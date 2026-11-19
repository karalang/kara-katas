// LeetCode #1629: Slowest Key -- the bench's Rust mirror: the ★ arm on
// 1000 random problems of 1000 presses, all drawn first, each answered 100
// times.

fn slowest_key(release_times: &[i32], keys_pressed: &str) -> char {
    let mut previous = 0;
    let mut best = (0, 'a');
    for (&time, key) in release_times.iter().zip(keys_pressed.chars()) {
        best = best.max((time - previous, key));
        previous = time;
    }
    best.1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1629;
    let mut problems: Vec<(Vec<i32>, String)> = Vec::new();
    for _ in 0..1000 {
        let mut release_times = Vec::new();
        let mut keys_pressed = String::new();
        let mut time: i64 = 0;
        for _ in 0..1000 {
            time += next_random(&mut seed) % 1000 + 1;
            release_times.push(time as i32);
            keys_pressed.push((b'a' + (next_random(&mut seed) % 26) as u8) as char);
        }
        problems.push((release_times, keys_pressed));
    }
    let mut check: i64 = 0;
    for _ in 0..100 {
        for (release_times, keys_pressed) in &problems {
            let key = slowest_key(release_times, keys_pressed);
            check = (check * 31 + key as i64) % 1000000007;
        }
    }
    println!("1000 problems of 1000 presses, answered 100 times: checksum {}", check);
}
