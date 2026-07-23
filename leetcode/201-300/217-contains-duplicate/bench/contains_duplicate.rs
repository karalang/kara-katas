use std::collections::HashSet;

fn window_has_dup(base: &[i64], w: i64, width: i64) -> bool {
    let mut seen: HashSet<i64> = HashSet::new();
    for t in 0..width {
        let x = base[(w + t) as usize];
        if seen.contains(&x) {
            return true;
        }
        seen.insert(x);
    }
    false
}

fn main() {
    let big: i64 = 240000;
    let width: i64 = 800;
    let m: i64 = 2000000;

    let mut base: Vec<i64> = Vec::new();
    let mut state: i64 = 12345;
    for _ in 0..big {
        state = (state * 1103515245 + 12345) & 2147483647;
        base.push(state % m);
    }

    let windows = big - width;
    let mut sink: i64 = 0;
    for w in 0..windows {
        if window_has_dup(&base, w, width) {
            sink += 1;
        }
    }
    println!("{}", sink);
}
