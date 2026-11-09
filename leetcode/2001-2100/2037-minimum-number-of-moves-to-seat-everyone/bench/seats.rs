// LeetCode #2037: Minimum Number of Moves to Seat Everyone -- the ★ arm in
// Rust, the same algorithm and workload as seats.kara: both lists sorted,
// the k-th seat paired with the k-th student, the distances summed.

fn min_moves_to_seat(mut seats: Vec<i64>, mut students: Vec<i64>) -> i64 {
    seats.sort();
    students.sort();
    seats.iter().zip(students.iter()).map(|(a, b)| (a - b).abs()).sum()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2037;
    let mut seats: Vec<Vec<i64>> = Vec::new();
    let mut students: Vec<Vec<i64>> = Vec::new();
    for _ in 0..2000 {
        let a: Vec<i64> = (0..100).map(|_| next_random(&mut seed) % 100 + 1).collect();
        let b: Vec<i64> = (0..100).map(|_| next_random(&mut seed) % 100 + 1).collect();
        seats.push(a);
        students.push(b);
    }
    let mut calls = 0;
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..25 {
        for r in 0..2000 {
            let at = (round * 37 + r * 11) % 100;
            seats[r][at] = seats[r][at] % 100 + 1;
            let answer = min_moves_to_seat(seats[r].clone(), students[r].clone());
            calls += 1;
            sum += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    println!("{} calls: sum {}, checksum {}", calls, sum, check);
}
