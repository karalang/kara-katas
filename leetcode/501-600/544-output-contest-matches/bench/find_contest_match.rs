// Benchmark for #544: Rust mirror of the ★ arm (rounds, in place); see
// find_contest_match.kara.

fn find_contest_match(n: i64) -> String {
    let mut teams: Vec<String> = (1..n + 1).map(|t| format!("{t}")).collect();
    let mut m = n as usize;
    while m > 1 {
        for i in 0..m / 2 {
            teams[i] = format!("({},{})", teams[i], teams[m - 1 - i]);
        }
        m /= 2;
    }
    teams[0].clone()
}

fn main() {
    // 200 rounds over every size the problem allows, 2 to 4,096 teams;
    // the length of each answer is summed, and one byte of it, picked
    // by the round and the size, goes into the checksum.
    let mut total = 0;
    let mut checksum: i64 = 0;
    for r in 0..200i64 {
        let mut n = 2i64;
        while n <= 4096 {
            let s = find_contest_match(n);
            let b = s.as_bytes()[((r * 7919 + n * 13) % s.len() as i64) as usize] as i64;
            total += s.len();
            checksum = (checksum * 31 + b) % 1000000007;
            n *= 2;
        }
    }
    println!("200 rounds of 2 to 4096 teams: {total} bytes, checksum {checksum}");
}
