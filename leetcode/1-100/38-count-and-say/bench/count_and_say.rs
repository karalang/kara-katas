// LeetCode #38 bench — Rust (mirror of count_and_say.kara).
//
// Streaming run-length "say" over a growing `String`. Workload: TOTAL times seed with the
// decimal digits of k+1, apply STEPS say-steps, fold a position-weighted digit signature
// of the final term into a checksum. `rustc -O` wraps on overflow; the bench also builds a
// `-C overflow-checks=on` variant to match Kāra's checked-by-default semantics (all values
// stay well inside i64, so neither variant traps — the safety tax isolates codegen).

fn say(s: &str) -> String {
    // Run lengths stay <= 9 in this workload (verified max 5), so the count is a
    // single decimal digit appended in place — fair, allocation-free across mirrors.
    let mut out = String::new();
    let mut run_digit: u8 = b'0';
    let mut run_len: i64 = 0;
    for &c in s.as_bytes() {
        if run_len != 0 && c == run_digit {
            run_len += 1;
        } else {
            if run_len != 0 {
                out.push((b'0' + run_len as u8) as char);
                out.push(run_digit as char);
            }
            run_digit = c;
            run_len = 1;
        }
    }
    if run_len != 0 {
        out.push((b'0' + run_len as u8) as char);
        out.push(run_digit as char);
    }
    out
}

fn main() {
    let total: i64 = 12000;
    let steps: i64 = 14;
    let modulus: i64 = 1000000007;

    let mut acc: i64 = 0;
    for k in 0..total {
        let mut cur = (k + 1).to_string();
        for _ in 0..steps {
            cur = say(&cur);
        }

        let mut sig: i64 = 0;
        for (i, &c) in cur.as_bytes().iter().enumerate() {
            let dv = (c - b'0') as i64;
            sig += dv * (i as i64 + 1);
        }
        acc = (acc * 31 + sig) % modulus;
    }

    println!("{}", acc);
}
