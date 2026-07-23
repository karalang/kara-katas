// Benchmark workload for LeetCode #210 — Course Schedule II.
const MOD: i64 = 1000000007;
const BIG: i64 = 1000000;

fn main() {
    let n: i64 = 20000;
    let e: i64 = 80000;
    let passes: i64 = 800;

    let mut eb: Vec<i64> = Vec::new();
    let mut ea: Vec<i64> = Vec::new();
    let mut outdeg: Vec<i64> = vec![0; n as usize];
    let mut indeg0: Vec<i64> = vec![0; n as usize];

    let mut state: i64 = 12345;
    for _ in 0..e {
        state = (state * 1103515245 + 12345) & 2147483647;
        let b = state % (n - 1); // 0 .. n-2
        state = (state * 1103515245 + 12345) & 2147483647;
        let a = b + 1 + state % (n - 1 - b); // b+1 .. n-1 (b < a => DAG)
        eb.push(b);
        ea.push(a);
        outdeg[b as usize] += 1;
        indeg0[a as usize] += 1;
    }

    // CSR build.
    let mut adj_start: Vec<i64> = vec![0; (n + 1) as usize];
    for i in 0..n {
        adj_start[(i + 1) as usize] = adj_start[i as usize] + outdeg[i as usize];
    }
    let mut adj_flat: Vec<i64> = vec![0; e as usize];
    let mut cursor: Vec<i64> = vec![0; n as usize];
    for i in 0..n {
        cursor[i as usize] = adj_start[i as usize];
    }
    for i in 0..e {
        let src = eb[i as usize];
        adj_flat[cursor[src as usize] as usize] = ea[i as usize];
        cursor[src as usize] += 1;
    }

    let mut indeg: Vec<i64> = vec![0; n as usize];
    let mut queue: Vec<i64> = vec![0; n as usize];

    let mut sink: i64 = 0;
    for p in 0..passes {
        for i in 0..n as usize {
            indeg[i] = indeg0[i];
        }
        let blocked = (p % n) as usize;
        indeg[blocked] += BIG;

        let mut head: i64 = 0;
        let mut tail: i64 = 0;
        for c in 0..n {
            if indeg[c as usize] == 0 {
                queue[tail as usize] = c;
                tail += 1;
            }
        }
        let mut checksum: i64 = 0;
        let mut cnt: i64 = 0;
        while head < tail {
            let node = queue[head as usize];
            head += 1;
            checksum = (checksum + node * (cnt + 1)) % MOD;
            cnt += 1;
            let start = adj_start[node as usize];
            let end = adj_start[(node + 1) as usize];
            for j in start..end {
                let nb = adj_flat[j as usize];
                indeg[nb as usize] -= 1;
                if indeg[nb as usize] == 0 {
                    queue[tail as usize] = nb;
                    tail += 1;
                }
            }
        }
        sink += cnt + checksum;
    }

    println!("{}", sink);
}
