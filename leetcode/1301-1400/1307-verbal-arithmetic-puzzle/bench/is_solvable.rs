// LeetCode #1307 bench in Rust: the ★ arm (the sum done a column at a time
// from the right with its carry, the result's letter fixed by each column's
// sum) on the same 40 passes of 50 puzzles.

struct Puzzle {
    // each word and the result as letter numbers, rightmost first
    words: Vec<Vec<usize>>,
    result: Vec<usize>,
    leads: Vec<bool>,
    digit: Vec<i64>,
    taken: [bool; 10],
}

fn solve(p: &mut Puzzle, col: usize, row: usize, sum: i64) -> bool {
    if col == p.result.len() {
        return sum == 0;
    }
    if row == p.words.len() {
        let letter = p.result[col];
        let d = sum % 10;
        if p.digit[letter] >= 0 {
            return p.digit[letter] == d && solve(p, col + 1, 0, sum / 10);
        }
        if p.taken[d as usize] || (d == 0 && p.leads[letter]) {
            return false;
        }
        p.digit[letter] = d;
        p.taken[d as usize] = true;
        let ok = solve(p, col + 1, 0, sum / 10);
        p.digit[letter] = -1;
        p.taken[d as usize] = false;
        return ok;
    }
    if col >= p.words[row].len() {
        return solve(p, col, row + 1, sum);
    }
    let letter = p.words[row][col];
    if p.digit[letter] >= 0 {
        let d = p.digit[letter];
        return solve(p, col, row + 1, sum + d);
    }
    for d in 0..10i64 {
        if p.taken[d as usize] || (d == 0 && p.leads[letter]) {
            continue;
        }
        p.digit[letter] = d;
        p.taken[d as usize] = true;
        let ok = solve(p, col, row + 1, sum + d);
        p.digit[letter] = -1;
        p.taken[d as usize] = false;
        if ok {
            return true;
        }
    }
    false
}

fn is_solvable(words: &[String], result: &str) -> bool {
    if words.iter().any(|w| w.len() > result.len()) {
        return false;
    }
    let mut number = [usize::MAX; 26];
    let mut leads: Vec<bool> = Vec::new();
    let mut rows: Vec<Vec<usize>> = Vec::new();
    for text in words.iter().map(|w| w.as_str()).chain(std::iter::once(result)) {
        let mut row: Vec<usize> = Vec::new();
        for c in text.bytes() {
            let k = (c - b'A') as usize;
            if number[k] == usize::MAX {
                number[k] = leads.len();
                leads.push(false);
            }
            row.push(number[k]);
        }
        if row.len() > 1 {
            leads[row[0]] = true;
        }
        row.reverse();
        rows.push(row);
    }
    let result_row = rows.pop().unwrap();
    let letters = leads.len();
    let mut p = Puzzle { words: rows, result: result_row, leads, digit: vec![-1; letters], taken: [false; 10] };
    solve(&mut p, 0, 0, 0)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut check: i64 = 0;
    for pass in 0..40i64 {
        let mut seed = check;
        let mut solvable = 0i64;
        for p in 0..50 {
            let mut letter: Vec<u8> = b"ABCDEFGHIJ".to_vec();
            for k in (1..10).rev() {
                let j = (next_random(&mut seed) % (k as i64 + 1)) as usize;
                letter.swap(k, j);
            }
            let count = 2 + next_random(&mut seed) % 4;
            let mut numbers: Vec<i64> = Vec::new();
            for _ in 0..count {
                let digits = 1 + next_random(&mut seed) % 6;
                let mut low = 1i64;
                for _ in 1..digits {
                    low *= 10;
                }
                let value = if digits == 1 { next_random(&mut seed) % 10 } else { low + next_random(&mut seed) % (9 * low) };
                numbers.push(value);
            }
            let total: i64 = numbers.iter().sum();
            numbers.push(total);
            let mut texts: Vec<String> = numbers
                .iter()
                .map(|v| v.to_string().bytes().map(|c| letter[(c - b'0') as usize] as char).collect())
                .collect();
            let mut result = texts.pop().unwrap();
            if p % 2 == 1 {
                let mut chars: Vec<u8> = result.into_bytes();
                let at = (next_random(&mut seed) % chars.len() as i64) as usize;
                chars[at] = letter[(next_random(&mut seed) % 10) as usize];
                result = String::from_utf8(chars).unwrap();
            }
            if is_solvable(&texts, &result) {
                solvable += 1;
            }
        }
        check = (check * 31 + solvable + pass) % 1000000007;
    }
    println!("40 passes of 50 puzzles: checksum {check}");
}
