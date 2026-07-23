// Benchmark workload for LeetCode #211 — Add and Search Words Data Structure.
const ALPHA: usize = 6;
const WLEN: usize = 6;

fn dfs(children: &[i64], is_end: &[i64], wild: &[i64], letter: &[i64], cur: usize, pos: usize) -> bool {
    if pos == WLEN {
        return is_end[cur] == 1;
    }
    if wild[pos] == 1 {
        for a in 0..ALPHA {
            let nc = children[cur * ALPHA + a];
            if nc != 0 && dfs(children, is_end, wild, letter, nc as usize, pos + 1) {
                return true;
            }
        }
        return false;
    }
    let nc = children[cur * ALPHA + letter[pos] as usize];
    if nc == 0 {
        return false;
    }
    dfs(children, is_end, wild, letter, nc as usize, pos + 1)
}

fn main() {
    let nwords: i64 = 20000;
    let nquery: i64 = 8000000;

    let mut children: Vec<i64> = vec![0; ALPHA]; // root at index 0
    let mut is_end: Vec<i64> = vec![0];

    let mut state: i64 = 12345;

    // Build phase.
    for _ in 0..nwords {
        let mut cur: usize = 0;
        for _ in 0..WLEN {
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
    let mut wild: Vec<i64> = vec![0; WLEN];
    let mut letter: Vec<i64> = vec![0; WLEN];
    let mut sink: i64 = 0;
    for _ in 0..nquery {
        for k in 0..WLEN {
            state = (state * 1103515245 + 12345) & 2147483647;
            let v = state;
            wild[k] = if v % 6 == 0 { 1 } else { 0 };
            letter[k] = (v / 6) % ALPHA as i64;
        }
        if dfs(&children, &is_end, &wild, &letter, 0, 0) {
            sink += 1;
        }
    }

    println!("{}", sink);
}
