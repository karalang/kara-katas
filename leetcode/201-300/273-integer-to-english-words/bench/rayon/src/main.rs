// Benchmark workload for LeetCode #273 — Integer to English Words.
//
// PARALLEL LANE (rayon). Algorithm-for-algorithm mirror of spell.kara. See that file's header for what
// this lane measures and for the parity decisions — in particular that the
// algorithm PREPENDS, which is preserved here rather than rewritten into an
// append that would let this mirror amortize into one growing buffer.

const SMALL: [&str; 20] = ["", "One", "Two", "Three", "Four", "Five", "Six",
    "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen",
    "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"];
const TENS: [&str; 10] = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty",
    "Seventy", "Eighty", "Ninety"];
const SCALES: [&str; 4] = ["", "Thousand", "Million", "Billion"];

fn group_name(n: i64) -> String {
    if n == 0 {
        return String::new();
    }
    if n < 20 {
        return SMALL[n as usize].to_string();
    }
    if n < 100 {
        let t = TENS[(n / 10) as usize].to_string();
        let r = n % 10;
        if r == 0 {
            return t;
        }
        return t + " " + SMALL[r as usize];
    }
    let h = SMALL[(n / 100) as usize].to_string() + " " + "Hundred";
    let r = group_name(n % 100);
    if r.is_empty() {
        return h;
    }
    h + " " + &r
}

fn number_to_words(n: i64) -> String {
    if n == 0 {
        return "Zero".to_string();
    }
    let mut out = String::new();
    let mut rem = n;
    let mut scale = 0i64;
    while rem > 0 {
        let part = rem % 1000;
        if part > 0 {
            let mut piece = group_name(part);
            if scale > 0 {
                piece = piece + " " + SCALES[scale as usize];
            }
            out = if out.is_empty() { piece } else { piece + " " + &out };
        }
        rem /= 1000;
        scale += 1;
    }
    out
}

use rayon::prelude::*;

fn main() {
    let count: i64 = 200000;
    let rounds: i64 = 5;

    let mut nums: Vec<i64> = Vec::with_capacity(count as usize);
    let mut lo: i64 = 2147483647;
    let mut hi: i64 = 0;
    let mut state: i64 = 273273;
    for _ in 0..count {
        state = (state * 1103515245 + 12345) & 2147483647;
        if state < lo { lo = state; }
        if state > hi { hi = state; }
        nums.push(state);
    }

    let total = count * rounds;
    // Per-item hash, summed — order-invariant across items, which is what lets
    // this be a parallel reduction at all.
    let sink: i64 = (0..total)
        .into_par_iter()
        .map(|t| {
            let w = number_to_words(nums[(t % count) as usize]);
            let mut h: i64 = 0;
            for b in w.as_bytes() {
                h = (h * 131 + *b as i64) % 1000000007;
            }
            h
        })
        .reduce(|| 0i64, |a, b| (a + b) % 1000000007);

    println!("{sink}");
    println!("spellings {total} range {lo}..{hi}");
}
