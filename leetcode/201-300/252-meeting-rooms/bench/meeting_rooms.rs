// Benchmark workload for LeetCode #252 — Meeting Rooms (Rust mirror).
// Mirrors meeting_rooms.kara algorithm-for-algorithm: one packed attendable set
// built and shuffled once, then per round a fresh copy sorted by start and
// scanned to completion.

fn main() {
    let n: i64 = 120000;
    let rounds: i64 = 40;

    let mut base: Vec<(i64, i64)> = Vec::with_capacity(n as usize);
    let mut state: i64 = 252252;
    let mut cursor: i64 = 0;
    for _ in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        let dur = (state / 65536) % 7 + 1;
        state = (state * 1103515245 + 12345) & 2147483647;
        let gap = (state / 65536) % 3;
        base.push((cursor, cursor + dur));
        cursor += dur + gap;
    }
    let mut k = base.len() as i64 - 1;
    while k > 0 {
        state = (state * 1103515245 + 12345) & 2147483647;
        let wd0 = state / 65536;
        state = (state * 1103515245 + 12345) & 2147483647;
        let swap = (wd0 * 32768 + state / 65536) % (k + 1);
        base.swap(k as usize, swap as usize);
        k -= 1;
    }

    let mut sink: i64 = 0;
    for _ in 0..rounds {
        let mut s: Vec<(i64, i64)> = base.clone();
        s.sort_by(|a, b| a.0.cmp(&b.0));

        let mut ok = true;
        for j in 1..n as usize {
            if s[j].0 < s[j - 1].1 {
                ok = false;
            }
        }
        sink = if ok { (sink * 31 + 1) % 1000000007 } else { (sink * 31) % 1000000007 };
        sink = (sink * 131 + s[n as usize - 1].1 - s[0].0) % 1000000007;
    }
    println!("{}", sink);
}
