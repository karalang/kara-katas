// Benchmark workload for LeetCode #255 — Verify Preorder Sequence in BST (Rust mirror).
// Mirrors verify_preorder.kara algorithm-for-algorithm: random BST built once,
// preorder emitted, then repeated ancestor-stack verification.

fn main() {
    let n: i64 = 200000;
    let rounds: i64 = 250;

    let mut val: Vec<i64> = Vec::new();
    let mut left: Vec<i64> = Vec::new();
    let mut right: Vec<i64> = Vec::new();
    let mut state: i64 = 255255;

    for _ in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        let v = state;
        if val.is_empty() {
            val.push(v); left.push(-1); right.push(-1);
        } else {
            let mut cur: i64 = 0;
            let mut placed = false;
            while !placed {
                if v == val[cur as usize] {
                    placed = true;
                } else if v < val[cur as usize] {
                    if left[cur as usize] == -1 {
                        val.push(v); left.push(-1); right.push(-1);
                        left[cur as usize] = val.len() as i64 - 1;
                        placed = true;
                    } else { cur = left[cur as usize]; }
                } else {
                    if right[cur as usize] == -1 {
                        val.push(v); left.push(-1); right.push(-1);
                        right[cur as usize] = val.len() as i64 - 1;
                        placed = true;
                    } else { cur = right[cur as usize]; }
                }
            }
        }
    }

    let mut preorder: Vec<i64> = Vec::new();
    let mut walk: Vec<i64> = vec![0];
    while let Some(node) = walk.pop() {
        if node != -1 {
            preorder.push(val[node as usize]);
            if right[node as usize] != -1 { walk.push(right[node as usize]); }
            if left[node as usize] != -1 { walk.push(left[node as usize]); }
        }
    }

    let m = preorder.len();
    let mut sink: i64 = 0;
    for _ in 0..rounds {
        let mut stack: Vec<i64> = Vec::new();
        let mut lower: i64 = i64::MIN;
        let mut ok = true;
        for k in 0..m {
            let x = preorder[k];
            if x < lower { ok = false; }
            while !stack.is_empty() && *stack.last().unwrap() < x {
                lower = stack.pop().unwrap();
            }
            stack.push(x);
        }
        sink = if ok { (sink * 31 + 1) % 1000000007 } else { (sink * 31) % 1000000007 };
        sink = (sink * 131 + (lower % 1000000007)) % 1000000007;
    }
    println!("{} {}", m, sink);
}
