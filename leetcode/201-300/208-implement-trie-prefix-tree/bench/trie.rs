// Benchmark workload for LeetCode #208 — Implement Trie (Prefix Tree).
const ALPHA: usize = 5;

fn main() {
    let nwords: i64 = 30000;
    let nquery: i64 = 8000000;

    let mut children: Vec<i64> = vec![0; ALPHA];
    let mut is_end: Vec<i64> = vec![0]; // root at index 0

    let mut state: i64 = 12345;

    // Build phase.
    for _ in 0..nwords {
        state = (state * 1103515245 + 12345) & 2147483647;
        let len = 2 + state % 7;
        let mut cur: usize = 0;
        for _ in 0..len {
            state = (state * 1103515245 + 12345) & 2147483647;
            let c = (state % ALPHA as i64) as usize;
            let nxt = children[cur * ALPHA + c];
            if nxt == 0 {
                let idx = is_end.len() as i64;
                for _ in 0..ALPHA {
                    children.push(0);
                }
                is_end.push(0);
                children[cur * ALPHA + c] = idx;
                cur = idx as usize;
            } else {
                cur = nxt as usize;
            }
        }
        is_end[cur] = 1;
    }

    // Query phase.
    let mut sink: i64 = 0;
    for _ in 0..nquery {
        state = (state * 1103515245 + 12345) & 2147483647;
        let len = 2 + state % 7;
        let mut cur: usize = 0;
        let mut alive = true;
        for _ in 0..len {
            state = (state * 1103515245 + 12345) & 2147483647;
            let c = (state % ALPHA as i64) as usize;
            if alive {
                let nxt = children[cur * ALPHA + c];
                if nxt == 0 {
                    alive = false;
                } else {
                    cur = nxt as usize;
                }
            }
        }
        if alive {
            sink += 1;
            if is_end[cur] == 1 {
                sink += 2;
            }
        }
    }

    println!("{}", sink);
}
