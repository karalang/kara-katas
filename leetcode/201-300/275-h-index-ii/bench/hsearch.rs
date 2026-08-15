// Benchmark workload for LeetCode #275 — H-Index II.
//
// Algorithm-for-algorithm mirror of hsearch.kara. See that file's header for
// what this lane measures and why the array is sized at 2 MiB.

fn h_index_prefix(citations: &[i64], n: i64) -> i64 {
    let mut lo: i64 = 0;
    let mut hi: i64 = n;
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if citations[mid as usize] >= n - mid { hi = mid; } else { lo = mid + 1; }
    }
    n - lo
}

fn main() {
    let size: i64 = 262144;
    let queries: i64 = 6000000;

    let mut citations: Vec<i64> = Vec::with_capacity(size as usize);
    let mut state: i64 = 275275;
    let mut cur: i64 = 0;
    for _ in 0..size {
        state = (state * 1103515245 + 12345) & 2147483647;
        cur += (state / 256) % 3;
        citations.push(cur);
    }
    let top = citations[(size - 1) as usize];

    let mut sink: i64 = 0;
    for _ in 0..queries {
        state = (state * 1103515245 + 12345) & 2147483647;
        let n = 1 + (state / 256) % size;
        sink = (sink * 131 + h_index_prefix(&citations, n)) % 1000000007;
    }

    println!("{sink}");
    println!("size {size} queries {queries} top {top}");
}
