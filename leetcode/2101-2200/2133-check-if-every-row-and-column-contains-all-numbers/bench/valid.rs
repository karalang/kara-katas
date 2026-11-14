// LeetCode #2133: Check if Every Row and Column Contains All Numbers --
// the benchmark, the same algorithm as valid.kara.

fn check_valid(matrix: &[Vec<i64>]) -> bool {
    let n = matrix.len();
    let mut mark = vec![-1i64; n + 1];
    for i in 0..n {
        let line = 2 * i as i64;
        for j in 0..n {
            let v = matrix[i][j] as usize;
            if mark[v] == line {
                return false;
            }
            mark[v] = line;
        }
        for j in 0..n {
            let v = matrix[j][i] as usize;
            if mark[v] == line + 1 {
                return false;
            }
            mark[v] = line + 1;
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn latin(n: i64, seed: &mut i64) -> Vec<Vec<i64>> {
    let mut rows: Vec<i64> = (0..n).collect();
    let mut symbols: Vec<i64> = (1..n + 1).collect();
    for i in (1..n).rev() {
        let j = next_random(seed) % (i + 1);
        rows.swap(i as usize, j as usize);
        let j = next_random(seed) % (i + 1);
        symbols.swap(i as usize, j as usize);
    }
    (0..n)
        .map(|r| (0..n).map(|c| symbols[((rows[r as usize] + c) % n) as usize]).collect())
        .collect()
}

fn main() {
    let mut seed = 2133i64;
    let mut squares: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..10 {
        squares.push(latin(100, &mut seed));
    }
    let mut valid = 0i64;
    let mut check = 0i64;
    for round in 0..20000 {
        let k = (next_random(&mut seed) % 10) as usize;
        let r = (next_random(&mut seed) % 100) as usize;
        let a = (next_random(&mut seed) % 100) as usize;
        let b = (next_random(&mut seed) % 100) as usize;
        let ok;
        if round % 2 == 1 {
            squares[k].swap(a, b);
            ok = check_valid(&squares[k]);
        } else {
            squares[k][r].swap(a, b);
            ok = check_valid(&squares[k]);
            squares[k][r].swap(a, b);
        }
        let x = if ok { 1 } else { 0 };
        valid += x;
        check = (check * 31 + x + squares[k][r][a]) % 1000000007;
    }
    println!("20000 solves: {} valid, checksum {}", valid, check);
}
