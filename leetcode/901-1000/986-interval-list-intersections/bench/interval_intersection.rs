// Benchmark: LeetCode #986 Interval List Intersections -- the ★ arm, two pointers,
// on pairs of LeetCode's largest lists, 1000 intervals each.
// Mirrors interval_intersection.kara, .c, .py and go-seq/.

fn interval_intersection(first: &[(i64, i64)], second: &[(i64, i64)]) -> Vec<(i64, i64)> {
    let mut out = Vec::new();
    let mut i = 0;
    let mut j = 0;
    while i < first.len() && j < second.len() {
        let (a_start, a_end) = first[i];
        let (b_start, b_end) = second[j];
        let lo = a_start.max(b_start);
        let hi = a_end.min(b_end);
        if lo <= hi {
            out.push((lo, hi));
        }
        if a_end < b_end {
            i += 1;
        } else {
            j += 1;
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn random_list(seed: &mut i64) -> Vec<(i64, i64)> {
    let mut out = Vec::new();
    let mut pos = wide_random(seed) % 499999;
    for _ in 0..1000 {
        let start = pos;
        let end = start + 1 + wide_random(seed) % 499999;
        out.push((start, end));
        pos = end + 1 + wide_random(seed) % 499999;
    }
    out
}

fn main() {
    let rounds = 1000;
    let mut seed = 986;
    let mut lists = Vec::new();
    for _ in 0..21 {
        lists.push(random_list(&mut seed));
    }
    let mut found: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..20 {
            let k = (r + i) % 20;
            let answer = interval_intersection(&lists[k], &lists[k + 1]);
            found += answer.len() as i64;
            let (lo, hi) = answer[answer.len() / 2];
            check = (check * 31 + answer.len() as i64 + lo % 1000 + hi % 1000) % 1000000007;
        }
    }
    println!("{} rounds over 20 pairs of 1000 intervals: {} intersections, checksum {}", rounds, found, check);
}
