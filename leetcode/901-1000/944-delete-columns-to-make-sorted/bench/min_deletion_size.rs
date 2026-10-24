// Benchmark: LeetCode #944 Delete Columns to Make Sorted -- the ★ arm,
// column by column, on grids of 100 rows of 1000 letters, LeetCode's
// largest. Mirrors min_deletion_size.kara, .c, .py and go-seq/.

fn min_deletion_size(strs: &[String]) -> i64 {
    let rows: Vec<&[u8]> = strs.iter().map(|s| s.as_bytes()).collect();
    let n = rows.len();
    let m = rows[0].len();
    let mut deleted = 0;
    for c in 0..m {
        let mut r = 1;
        while r < n && rows[r - 1][c] <= rows[r][c] {
            r += 1;
        }
        if r < n {
            deleted += 1;
        }
    }
    deleted
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let (rounds, count, n, m) = (150, 20, 100usize, 1000usize);
    let mut seed = 944;
    let mut grids: Vec<Vec<String>> = Vec::new();
    for _ in 0..count {
        let mut columns: Vec<Vec<u8>> = Vec::new();
        for _ in 0..m {
            let mut column: Vec<u8> = (0..n)
                .map(|_| (next_random(&mut seed) % 26 + 97) as u8)
                .collect();
            column.sort();
            if next_random(&mut seed) % 2 == 0 {
                let a = (next_random(&mut seed) % n as i64) as usize;
                let b = (next_random(&mut seed) % n as i64) as usize;
                column.swap(a, b);
            }
            columns.push(column);
        }
        let strs: Vec<String> = (0..n)
            .map(|r| (0..m).map(|c| columns[c][r] as char).collect())
            .collect();
        grids.push(strs);
    }
    let mut total = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let d = min_deletion_size(&grids[(r + i) % count]);
            total += d;
            check = (check * 1000003 + d * (i as i64 + 1)) % 1000000007;
        }
    }
    println!("{rounds} rounds over {count} grids of {n} rows of {m} letters: {total} deleted, checksum {check}");
}
