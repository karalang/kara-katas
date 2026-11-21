// LeetCode #2511: Maximum Enemy Forts That Can Be Captured -- Rust mirror
// of the benchmark (forts.kara): the same lines, passes and checksum.

fn capture_forts(forts: &[i64]) -> i64 {
    let mut best = 0;
    let mut last: i64 = -1;
    for i in 0..forts.len() {
        if forts[i] != 0 {
            if last >= 0 && forts[last as usize] == -forts[i] {
                best = best.max(i as i64 - last - 1);
            }
            last = i as i64;
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2511;
    let mut lines: Vec<Vec<i64>> = Vec::new();
    for k in 0..2000 {
        let zeros = k % 50 + 1;
        let mut line = Vec::new();
        for _ in 0..1000 {
            let r = next_random(&mut seed) % (zeros + 2);
            line.push(if r < zeros { 0 } else if r == zeros { 1 } else { -1 });
        }
        lines.push(line);
    }
    let passes = 115;
    let mut check: i64 = 0;
    for p in 0..passes {
        for line in lines.iter_mut() {
            let at = (check % 1000) as usize;
            let kept = line[at];
            line[at] = (check + p) % 3 - 1;
            check = (check * 31 + capture_forts(line) + p) % 1000000007;
            line[at] = kept;
        }
    }
    println!("{} passes over 2000 lines of 1000 forts: checksum {}", passes, check);
}
