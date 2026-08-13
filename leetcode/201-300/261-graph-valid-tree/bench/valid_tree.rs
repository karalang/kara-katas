// Benchmark workload for LeetCode #261 — Graph Valid Tree (Rust mirror).
// Mirrors valid_tree.kara algorithm-for-algorithm.

fn find(parent: &mut [i64], x: i64) -> i64 {
    let mut r = x;
    while parent[r as usize] != r {
        r = parent[r as usize];
    }
    let mut c = x;
    while parent[c as usize] != r {
        let nxt = parent[c as usize];
        parent[c as usize] = r;
        c = nxt;
    }
    r
}

fn main() {
    let n: i64 = 100000;
    let rounds: i64 = 240;
    let m = n - 1;

    let mut eu: Vec<i64> = Vec::with_capacity(m as usize);
    let mut ev: Vec<i64> = Vec::with_capacity(m as usize);
    let mut state: i64 = 261261;
    for i in 1..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        eu.push((state / 65536) % i);
        ev.push(i);
    }
    let mut sh = m - 1;
    while sh > 0 {
        state = (state * 1103515245 + 12345) & 2147483647;
        let j = (state / 65536) % (sh + 1);
        eu.swap(sh as usize, j as usize);
        ev.swap(sh as usize, j as usize);
        sh -= 1;
    }

    let mut parent: Vec<i64> = vec![0; n as usize];
    let mut size: Vec<i64> = vec![0; n as usize];

    let mut sink: i64 = 0;
    for r in 0..rounds {
        for k in 0..n {
            parent[k as usize] = k;
            size[k as usize] = 1;
        }

        let start = (r * 7919) % m;
        let mut components = n;
        let mut cyclic = false;
        let mut e: i64 = 0;
        while e < m {
            let idx = ((start + e) % m) as usize;
            let ra = find(&mut parent, eu[idx]);
            let rb = find(&mut parent, ev[idx]);
            if ra == rb {
                cyclic = true;
                e = m;
            } else {
                if size[ra as usize] < size[rb as usize] {
                    parent[ra as usize] = rb;
                    size[rb as usize] += size[ra as usize];
                } else {
                    parent[rb as usize] = ra;
                    size[ra as usize] += size[rb as usize];
                }
                components -= 1;
                e += 1;
            }
        }

        let mut acc: i64 = 0;
        for p in 0..n {
            acc = (acc * 31 + parent[p as usize]) % 1000000007;
        }
        let verdict: i64 = if components == 1 && !cyclic { 1 } else { 0 };
        sink = (sink * 131 + acc + verdict) % 1000000007;
    }

    println!("{}", sink);
}
