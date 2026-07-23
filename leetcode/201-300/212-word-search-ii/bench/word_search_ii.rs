// Benchmark workload for LeetCode #212 — Word Search II.
const ALPHA: usize = 6;
const SIZE: i64 = 12;

fn dfs(board: &mut [i64], children: &[i64], is_end: &mut [i64], r: i64, c: i64, node: i64) -> i64 {
    let cell = board[(r * SIZE + c) as usize];
    if cell == -1 {
        return 0;
    }
    let nxt = children[node as usize * ALPHA + cell as usize];
    if nxt == 0 {
        return 0;
    }
    let mut cnt = nxt; // checksum each descended node
    if is_end[nxt as usize] == 1 {
        is_end[nxt as usize] = 0; // collect each word once per run
        cnt += nxt; // + collected-word identity
    }
    board[(r * SIZE + c) as usize] = -1; // mark visited
    if r > 0 {
        cnt += dfs(board, children, is_end, r - 1, c, nxt);
    }
    if r + 1 < SIZE {
        cnt += dfs(board, children, is_end, r + 1, c, nxt);
    }
    if c > 0 {
        cnt += dfs(board, children, is_end, r, c - 1, nxt);
    }
    if c + 1 < SIZE {
        cnt += dfs(board, children, is_end, r, c + 1, nxt);
    }
    board[(r * SIZE + c) as usize] = cell; // restore
    cnt
}

fn main() {
    let nwords: i64 = 4000;
    let runs: i64 = 40000;
    let cells: i64 = SIZE * SIZE;

    let mut children: Vec<i64> = vec![0; ALPHA]; // root at index 0
    let mut is_end0: Vec<i64> = vec![0];

    let mut state: i64 = 12345;

    // Build trie once.
    for _ in 0..nwords {
        state = (state * 1103515245 + 12345) & 2147483647;
        let len = 5 + state % 4; // 5..8
        let mut cur: usize = 0;
        for _ in 0..len {
            state = (state * 1103515245 + 12345) & 2147483647;
            let ch = (state % ALPHA as i64) as usize;
            let nxt = children[cur * ALPHA + ch];
            if nxt == 0 {
                let idx = is_end0.len() as i64;
                for _ in 0..ALPHA {
                    children.push(0);
                }
                is_end0.push(0);
                children[cur * ALPHA + ch] = idx;
                cur = idx as usize;
            } else {
                cur = nxt as usize;
            }
        }
        is_end0[cur] = 1;
    }

    let nnodes = is_end0.len();
    let mut is_end: Vec<i64> = vec![0; nnodes];
    let mut board: Vec<i64> = vec![0; cells as usize];

    let mut sink: i64 = 0;
    for _ in 0..runs {
        is_end[..nnodes].copy_from_slice(&is_end0[..nnodes]);
        // Fresh board each run from the ongoing PRNG stream.
        for bi in 0..cells as usize {
            state = (state * 1103515245 + 12345) & 2147483647;
            board[bi] = state % ALPHA as i64;
        }
        let mut found: i64 = 0;
        for r in 0..SIZE {
            for c in 0..SIZE {
                found += dfs(&mut board, &children, &mut is_end, r, c, 0);
            }
        }
        sink += found;
    }

    println!("{}", sink);
}
