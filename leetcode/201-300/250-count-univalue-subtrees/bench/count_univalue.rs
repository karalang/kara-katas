// Benchmark workload for LeetCode #250 — Count Univalue Subtrees (Rust mirror).
// Mirrors count_univalue.kara algorithm-for-algorithm.

fn main() {
    let nodes_n: i64 = 2000000;
    let passes: i64 = 40;
    let alphabet: i64 = 3;

    let mut val: Vec<i64> = Vec::with_capacity(nodes_n as usize);
    let mut state: i64 = 250250;
    for _ in 0..nodes_n {
        state = (state * 1103515245 + 12345) & 2147483647;
        val.push((state / 65536) % alphabet);
    }

    let mut uni: Vec<bool> = vec![false; nodes_n as usize];

    let mut sink: i64 = 0;
    for _ in 0..passes {
        let mut total: i64 = 0;
        let mut j = nodes_n - 1;
        while j >= 0 {
            let left = 2 * j + 1;
            let right = 2 * j + 2;
            let mut ok = true;
            if left < nodes_n {
                if !uni[left as usize] || val[left as usize] != val[j as usize] {
                    ok = false;
                }
            }
            if right < nodes_n {
                if !uni[right as usize] || val[right as usize] != val[j as usize] {
                    ok = false;
                }
            }
            uni[j as usize] = ok;
            if ok {
                total += 1;
            }
            j -= 1;
        }
        sink = (sink + total) % 1000000007;
    }
    println!("{}", sink);
}
