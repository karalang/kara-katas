// Benchmark for #551: Rust mirror of the ★ arm (one pass, two counters);
// see student_attendance_record_i.kara.

fn check_record(s: &str) -> bool {
    let mut absences = 0;
    let mut lates = 0;
    for c in s.chars() {
        if c == 'L' {
            lates += 1;
            if lates == 3 {
                return false;
            }
        } else {
            lates = 0;
            if c == 'A' {
                absences += 1;
                if absences == 2 {
                    return false;
                }
            }
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 1000;
    let mut seed: i64 = 551;
    let mut records: Vec<String> = Vec::new();
    for _ in 0..count {
        let mut s = String::new();
        for _ in 0..1000 {
            let r = next_random(&mut seed) % 2000;
            s.push(if r < 1 { 'A' } else if r < 101 { 'L' } else { 'P' });
        }
        records.push(s);
    }
    let mut fine: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..300 {
        for g in 0..count {
            let bit = if check_record(&records[(round * 7 + g) % count]) { 1 } else { 0 };
            fine += bit;
            checksum = (checksum * 31 + bit + g as i64) % 1000000007;
        }
    }
    println!("{} records, 300 rounds each: {} fine, checksum {}", count, fine, checksum);
}
