// Benchmark for #552: Rust mirror of the ★ arm (six counters, rolled);
// see student_attendance_record_ii.kara.

fn check_record(n: i64) -> i64 {
    let m = 1000000007;
    let mut count = vec![1i64, 0, 0, 0, 0, 0];
    for _ in 0..n {
        let mut next = vec![0i64; 6];
        for a in 0..2 {
            for l in 0..3 {
                let c = count[a * 3 + l];
                if c == 0 {
                    continue;
                }
                next[a * 3] = (next[a * 3] + c) % m;
                if a == 0 {
                    next[3] = (next[3] + c) % m;
                }
                if l < 2 {
                    next[a * 3 + l + 1] = (next[a * 3 + l + 1] + c) % m;
                }
            }
        }
        count = next;
    }
    let mut total = 0;
    for c in count.iter() {
        total = (total + *c) % m;
    }
    total
}

fn main() {
    let mut checksum: i64 = 0;
    let mut days: i64 = 0;
    for k in 0..100i64 {
        let n = 100000 - (k * 997) % 1000;
        days += n;
        checksum = (checksum * 31 + check_record(n)) % 1000000007;
    }
    println!("100 lengths, {} days: checksum {}", days, checksum);
}
