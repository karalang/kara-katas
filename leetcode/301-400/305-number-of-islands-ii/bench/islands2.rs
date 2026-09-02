// Benchmark mirror — LeetCode 305, Number of Islands II.
// Same algorithm, same Fisher-Yates over the same LCG, same masked sink as
// islands2.kara. See ../README.md § Benchmarks.

fn main() {
    let n: i64 = 256;
    let cells: i64 = n * n;
    let passes: i64 = 160;

    let mut order: Vec<i64> = (0..cells).collect();
    let mut state: i64 = 20305;
    let mut i = cells - 1;
    while i > 0 {
        state = (state * 1103515245 + 12345) % 2147483648;
        let j = state % (i + 1);
        order.swap(i as usize, j as usize);
        i -= 1;
    }

    let mut parent: Vec<i64> = vec![0; cells as usize];
    let mut rank: Vec<i64> = vec![0; cells as usize];
    let mut checksum: i64 = 0;

    for _ in 0..passes {
        for k in 0..cells as usize {
            parent[k] = -1;
            rank[k] = 0;
        }
        let mut count: i64 = 0;
        for q in 0..cells as usize {
            let idx = order[q];
            let r = idx / n;
            let c = idx % n;
            parent[idx as usize] = idx;
            count += 1;
            for d in 0..4 {
                let mut nb: i64 = -1;
                if d == 0 && r > 0 { nb = idx - n; }
                if d == 1 && r < n - 1 { nb = idx + n; }
                if d == 2 && c > 0 { nb = idx - 1; }
                if d == 3 && c < n - 1 { nb = idx + 1; }
                if nb >= 0 && parent[nb as usize] >= 0 {
                    let mut ra = idx;
                    while parent[ra as usize] != ra { ra = parent[ra as usize]; }
                    let mut cur = idx;
                    while parent[cur as usize] != ra {
                        let nx = parent[cur as usize];
                        parent[cur as usize] = ra;
                        cur = nx;
                    }
                    let mut rb = nb;
                    while parent[rb as usize] != rb { rb = parent[rb as usize]; }
                    cur = nb;
                    while parent[cur as usize] != rb {
                        let nx = parent[cur as usize];
                        parent[cur as usize] = rb;
                        cur = nx;
                    }
                    if ra != rb {
                        if rank[ra as usize] < rank[rb as usize] {
                            parent[ra as usize] = rb;
                        } else if rank[ra as usize] > rank[rb as usize] {
                            parent[rb as usize] = ra;
                        } else {
                            parent[rb as usize] = ra;
                            rank[ra as usize] += 1;
                        }
                        count -= 1;
                    }
                }
            }
            checksum = (checksum + count) & 0x3FFFFFFF;
        }
    }
    println!("checksum {}", checksum);
}
