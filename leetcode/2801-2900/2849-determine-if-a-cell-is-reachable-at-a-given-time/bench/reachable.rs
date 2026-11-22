// LeetCode #2849: Determine if a Cell Is Reachable at a Given Time --
// the bench: the ★ arm over 10^6 random cases on LeetCode's grid, the
// finish within 3 of the start and t within 2 of the distance, all
// drawn first, then each answered 20 times.

fn is_reachable_at_time(sx: i64, sy: i64, fx: i64, fy: i64, t: i64) -> bool {
    if sx == fx && sy == fy {
        return t != 1;
    }
    (sx - fx).abs().max((sy - fy).abs()) <= t
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 1000000;
    let rounds = 20;
    let mut seed = 2849;
    let mut cases: Vec<(i64, i64, i64, i64, i64)> = Vec::new();
    for _ in 0..count {
        let sx = next_random(&mut seed) * 30000 % 1000000000 + 1;
        let sy = next_random(&mut seed) * 30000 % 1000000000 + 1;
        let fx = (sx + next_random(&mut seed) % 7 - 3).max(1).min(1000000000);
        let fy = if next_random(&mut seed) % 2 == 0 { sy } else { (sy + next_random(&mut seed) % 7 - 3).max(1).min(1000000000) };
        let d = (sx - fx).abs().max((sy - fy).abs());
        let t = (d + next_random(&mut seed) % 5 - 2).max(0);
        cases.push((sx, sy, fx, fy, t));
    }
    let mut yes = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for &(sx, sy, fx, fy, t) in cases.iter() {
            let ok = is_reachable_at_time(sx, sy, fx, fy, t);
            if ok {
                yes += 1;
            }
            check = (check * 3 + if ok { 2 } else { 1 } + r) % 1000000007;
        }
    }
    println!("{count} cases, {rounds} rounds: {yes} true, checksum {check}");
}
