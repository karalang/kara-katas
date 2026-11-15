// LeetCode #1578 bench: the same one pass, in Rust.

fn min_cost(colors: &str, needed_time: &[i64]) -> i64 {
    let cs = colors.as_bytes();
    let mut total = 0i64;
    let mut keep = 0i64;
    for i in 0..cs.len() {
        if i > 0 && cs[i] != cs[i - 1] {
            keep = 0;
        }
        total += keep.min(needed_time[i]);
        keep = keep.max(needed_time[i]);
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1578i64;
    let mut ropes: Vec<(String, Vec<i64>)> = Vec::new();
    for _ in 0..200 {
        let mut colors = String::new();
        let mut times: Vec<i64> = Vec::new();
        for _ in 0..100000 {
            colors.push((b'a' + (next_random(&mut seed) % 3) as u8) as char);
            times.push(next_random(&mut seed) % 1000 + 1);
        }
        ropes.push((colors, times));
    }
    let (mut check, mut total) = (0i64, 0i64);
    for (colors, times) in ropes.iter() {
        let cost = min_cost(colors, times);
        total += cost;
        check = mix(check, cost);
    }
    println!("200 ropes of 100000 balloons: time total {}, checksum {}", total, check);
}
