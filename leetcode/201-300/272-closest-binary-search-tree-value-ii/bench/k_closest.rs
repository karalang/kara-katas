// Benchmark workload for LeetCode #272 — Closest Binary Search Tree Value II.
//
// Algorithm-for-algorithm mirror of k_closest.kara. See that file's header for
// what this lane measures and for the three parity decisions (hoisted stacks,
// each language's own absolute value, targets that span the value range).

fn main() {
    let node_count: i64 = 30000;
    let target_count: i64 = 100000;
    let k: i64 = 8;
    let rounds: i64 = 10;
    let span: i64 = 1000000;

    let mut val: Vec<i64> = Vec::with_capacity(node_count as usize);
    let mut left: Vec<i64> = Vec::with_capacity(node_count as usize);
    let mut right: Vec<i64> = Vec::with_capacity(node_count as usize);
    let mut state: i64 = 272272;
    let mut placed: i64 = 0;
    let mut tries: i64 = 0;
    while placed < node_count && tries < node_count * 4 {
        state = (state * 1103515245 + 12345) & 2147483647;
        let v = (state / 256) % span;
        tries += 1;
        if val.is_empty() {
            val.push(v); left.push(-1); right.push(-1);
            placed += 1;
        } else {
            let mut cur: i64 = 0;
            let mut dup = false;
            let mut done = false;
            while !done {
                if v == val[cur as usize] {
                    dup = true;
                    done = true;
                } else if v < val[cur as usize] {
                    if left[cur as usize] < 0 {
                        val.push(v); left.push(-1); right.push(-1);
                        left[cur as usize] = val.len() as i64 - 1;
                        done = true;
                    } else {
                        cur = left[cur as usize];
                    }
                } else if right[cur as usize] < 0 {
                    val.push(v); left.push(-1); right.push(-1);
                    right[cur as usize] = val.len() as i64 - 1;
                    done = true;
                } else {
                    cur = right[cur as usize];
                }
            }
            if !dup {
                placed += 1;
            }
        }
    }
    let n = val.len() as i64;

    let mut targets: Vec<f64> = Vec::with_capacity(target_count as usize);
    let mut tmin = 0.0f64;
    let mut tmax = 0.0f64;
    for t in 0..target_count {
        state = (state * 1103515245 + 12345) & 2147483647;
        let whole = (state / 256) % span;
        state = (state * 1103515245 + 12345) & 2147483647;
        let frac = ((state / 256) % 1000) as f64 / 1000.0;
        let x = whole as f64 + frac;
        if t == 0 { tmin = x; tmax = x; }
        if x < tmin { tmin = x; }
        if x > tmax { tmax = x; }
        targets.push(x);
    }

    let depth_cap: usize = 256;
    let mut pred: Vec<i64> = vec![0; depth_cap];
    let mut succ: Vec<i64> = vec![0; depth_cap];
    let mut lower: Vec<i64> = vec![0; k as usize];
    let mut upper: Vec<i64> = vec![0; k as usize];
    let mut outv: Vec<i64> = vec![0; k as usize];

    let mut sink: i64 = 0;
    for _ in 0..rounds {
        for q in 0..target_count {
            let target = targets[q as usize];

            let mut pt: i64 = 0;
            let mut st: i64 = 0;
            let mut cur: i64 = 0;
            while cur >= 0 {
                if (val[cur as usize] as f64) < target {
                    pred[pt as usize] = cur;
                    pt += 1;
                    cur = right[cur as usize];
                } else {
                    succ[st as usize] = cur;
                    st += 1;
                    cur = left[cur as usize];
                }
            }

            let mut nl: i64 = 0;
            let mut nu: i64 = 0;
            let mut taken: i64 = 0;
            while taken < k && (pt > 0 || st > 0) {
                let mut take_pred = pt > 0;
                if pt > 0 && st > 0 {
                    let dp = (val[pred[(pt - 1) as usize] as usize] as f64 - target).abs();
                    let ds = (val[succ[(st - 1) as usize] as usize] as f64 - target).abs();
                    take_pred = dp <= ds;
                }
                if take_pred {
                    pt -= 1;
                    let node = pred[pt as usize];
                    let mut c = left[node as usize];
                    while c >= 0 {
                        pred[pt as usize] = c;
                        pt += 1;
                        c = right[c as usize];
                    }
                    lower[nl as usize] = val[node as usize];
                    nl += 1;
                } else {
                    st -= 1;
                    let node = succ[st as usize];
                    let mut c = right[node as usize];
                    while c >= 0 {
                        succ[st as usize] = c;
                        st += 1;
                        c = left[c as usize];
                    }
                    upper[nu as usize] = val[node as usize];
                    nu += 1;
                }
                taken += 1;
            }

            let mut w: i64 = 0;
            let mut i = nl - 1;
            while i >= 0 {
                outv[w as usize] = lower[i as usize];
                w += 1;
                i -= 1;
            }
            for j in 0..nu {
                outv[w as usize] = upper[j as usize];
                w += 1;
            }

            let mut acc: i64 = 0;
            for p in 0..w {
                acc = (acc * 31 + outv[p as usize]) % 1000000007;
            }
            sink = (sink * 131 + acc) % 1000000007;
        }
    }

    let mut vlo = val[0];
    let mut vhi = val[0];
    for m in 1..n {
        if val[m as usize] < vlo { vlo = val[m as usize]; }
        if val[m as usize] > vhi { vhi = val[m as usize]; }
    }
    println!("{sink}");
    println!("nodes {n} values {vlo}..{vhi} targets {}..{}", tmin as i64, tmax as i64);
}
