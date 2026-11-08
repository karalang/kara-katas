// LeetCode #2019: The Score of Students Solving Math Expression -- the ★ arm's
// benchmark, a mirror of score.kara: each run's values in a `HashSet`.
use std::collections::HashSet;

fn score_of_students(s: &str, answers: &[i64]) -> i64 {
    let chars: Vec<char> = s.chars().collect();
    let digits: Vec<i64> = chars.iter().step_by(2).map(|&c| c as i64 - '0' as i64).collect();
    let ops: Vec<char> = chars.iter().skip(1).step_by(2).cloned().collect();
    let n = digits.len();
    let mut sum = 0;
    let mut product = digits[0];
    for i in 0..n - 1 {
        if ops[i] == '+' {
            sum += product;
            product = digits[i + 1];
        } else {
            product *= digits[i + 1];
        }
    }
    let correct = sum + product;
    let mut values: Vec<Vec<HashSet<i64>>> = Vec::new();
    for i in 0..n {
        let mut row: Vec<HashSet<i64>> = Vec::new();
        for j in 0..n {
            let mut cell = HashSet::new();
            if i == j {
                cell.insert(digits[i]);
            }
            row.push(cell);
        }
        values.push(row);
    }
    for length in 2..n + 1 {
        for i in 0..n - length + 1 {
            let j = i + length - 1;
            let mut cell = HashSet::new();
            for k in i..j {
                for &a in values[i][k].iter() {
                    for &b in values[k + 1][j].iter() {
                        let v = if ops[k] == '+' { a + b } else { a * b };
                        if v <= 1000 {
                            cell.insert(v);
                        }
                    }
                }
            }
            values[i][j] = cell;
        }
    }
    let mut points = 0;
    for &answer in answers.iter() {
        if answer == correct {
            points += 5;
        } else if values[0][n - 1].contains(&answer) {
            points += 2;
        }
    }
    points
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 2019;
    let mut expressions: Vec<String> = Vec::new();
    let mut answer_lists: Vec<Vec<i64>> = Vec::new();
    for e in 0..200i64 {
        let top = e % 9 + 1;
        let times = e % 7 + 2;
        let mut s = String::new();
        for i in 0..16 {
            if i > 0 {
                s.push(if next_random(&mut seed) % 10 < times { '*' } else { '+' });
            }
            s.push((b'0' + (next_random(&mut seed) % (top + 1)) as u8) as char);
        }
        expressions.push(s);
        answer_lists.push((0..2000).map(|_| next_random(&mut seed) % 1001).collect());
    }
    let (mut calls, mut total, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..10 {
        for e in 0..expressions.len() {
            let points = score_of_students(&expressions[e], &answer_lists[e]);
            calls += 1;
            total += points;
            check = (check * 31 + points) % 1000000007;
        }
    }
    println!("{} calls: {} points, checksum {}", calls, total, check);
}
