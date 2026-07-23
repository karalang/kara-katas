fn main() {
    let n: i64 = 5000;
    let m: i64 = 15000;
    let passes: i64 = 8000;

    let mut esrc = vec![0i64; m as usize];
    let mut edst = vec![0i64; m as usize];
    let mut state: i64 = 12345;
    for e in 0..m as usize {
        state = (state * 1103515245 + 12345) & 2147483647;
        let s = state % n;
        state = (state * 1103515245 + 12345) & 2147483647;
        let d = state % n;
        esrc[e] = s;
        edst[e] = d;
    }

    let mut outdeg = vec![0i64; n as usize];
    let mut base_indeg = vec![0i64; n as usize];
    for e in 0..m as usize {
        outdeg[esrc[e] as usize] += 1;
        base_indeg[edst[e] as usize] += 1;
    }

    let mut offset = vec![0i64; (n + 1) as usize];
    let mut acc = 0i64;
    for c in 0..n as usize {
        acc += outdeg[c];
        offset[c + 1] = acc;
    }

    let mut adj = vec![0i64; m as usize];
    let mut cursor = vec![0i64; n as usize];
    for c in 0..n as usize {
        cursor[c] = offset[c];
    }
    for e in 0..m as usize {
        let sidx = cursor[esrc[e] as usize];
        adj[sidx as usize] = edst[e];
        cursor[esrc[e] as usize] = sidx + 1;
    }

    let mut indeg = vec![0i64; n as usize];
    let mut queue = vec![0i64; n as usize];

    let mut sink: i64 = 0;
    for p in 0..passes {
        for c in 0..n as usize {
            indeg[c] = base_indeg[c];
        }
        let blocked = (p % n) as usize;
        indeg[blocked] += 1;

        let mut qt: i64 = 0;
        for c in 0..n {
            if indeg[c as usize] == 0 {
                queue[qt as usize] = c;
                qt += 1;
            }
        }

        let mut qh: i64 = 0;
        let mut finished: i64 = 0;
        while qh < qt {
            let node = queue[qh as usize];
            qh += 1;
            finished += 1;
            let stop = offset[(node + 1) as usize];
            let mut k = offset[node as usize];
            while k < stop {
                let nb = adj[k as usize];
                indeg[nb as usize] -= 1;
                if indeg[nb as usize] == 0 {
                    queue[qt as usize] = nb;
                    qt += 1;
                }
                k += 1;
            }
        }
        sink += finished;
    }
    println!("{}", sink);
}
