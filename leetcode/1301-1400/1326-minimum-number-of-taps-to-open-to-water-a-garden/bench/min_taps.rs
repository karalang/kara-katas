// LeetCode #1326 bench, Rust mirror of the Kāra bench: the ★ arm (each tap
// turned into how far right it waters from its leftmost point, then the
// garden crossed as a jump game) on 20 gardens of 10^4 built once; then 300
// passes, each setting one tap of every garden from the checksum so far,
// answering it and folding the answer plus the pass into the checksum.

fn min_taps(n: i32, ranges: &[i32]) -> i32 {
    let n = n as i64;
    let mut farthest: Vec<i64> = vec![0; (n + 1) as usize];
    for i in 0..=n {
        let r = ranges[i as usize] as i64;
        let left = (i - r).max(0);
        let right = (i + r).min(n);
        farthest[left as usize] = farthest[left as usize].max(right);
    }
    let mut taps = 0;
    let mut watered = 0;
    let mut next = 0;
    for x in 0..n {
        next = next.max(farthest[x as usize]);
        if x == watered {
            if next <= x {
                return -1;
            }
            taps += 1;
            watered = next;
        }
    }
    taps
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: i64 = 10000;
    let mut seed = 1326i64;
    let mut gardens: Vec<Vec<i32>> = Vec::new();
    for t in 0..20 {
        let open = if t % 4 == 0 { 1 } else if t % 4 == 1 { 3 } else if t % 4 == 2 { 10 } else { 30 };
        let mut ranges: Vec<i32> = Vec::new();
        for _ in 0..=n {
            let r = if next_random(&mut seed) % open == 0 { 1 + next_random(&mut seed) % 100 } else { 0 };
            ranges.push(r as i32);
        }
        gardens.push(ranges);
    }
    let mut check: i64 = 0;
    for pass in 0..300i64 {
        for t in 0..20 {
            let ranges = &mut gardens[t];
            ranges[(check % (n + 1)) as usize] = ((check / 7) % 101) as i32;
            let taps = min_taps(n as i32, ranges) as i64;
            check = (check * 31 + taps + 1 + pass) % 1000000007;
        }
    }
    println!("300 passes over 20 gardens of 10^4: checksum {}", check);
}
