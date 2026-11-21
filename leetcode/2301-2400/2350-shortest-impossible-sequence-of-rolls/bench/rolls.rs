// LeetCode #2350: Shortest Impossible Sequence of Rolls -- the bench, the ★
// arm in Rust: the rolls cut greedily into pieces that each hold every
// face, with a table of the faces seen in the current piece made afresh at
// its end.

fn shortest_sequence(rolls: &[i64], k: i64) -> i64 {
    let mut seen = vec![false; (k + 1) as usize];
    let mut distinct = 0;
    let mut pieces = 0;
    for &r in rolls {
        if !seen[r as usize] {
            seen[r as usize] = true;
            distinct += 1;
            if distinct == k {
                pieces += 1;
                distinct = 0;
                seen = vec![false; (k + 1) as usize];
            }
        }
    }
    pieces + 1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 10 arrays of 10^5 rolls, of dice with 2 to 10^4 faces
    let faces = [2i64, 3, 6, 10, 20, 50, 100, 1000, 3000, 10000];
    let mut seed = 2350i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..10 {
        let k = faces[a];
        let mut rolls = Vec::new();
        for _ in 0..100000 {
            let high = next_random(&mut seed);
            rolls.push((high * 32768 + next_random(&mut seed)) % k + 1);
        }
        arrays.push(rolls);
    }
    let mut check = 0i64;
    for p in 0..50i64 {
        for a in 0..10 {
            check = (check * 31 + shortest_sequence(&arrays[a], faces[a]) + p) % 1000000007;
        }
    }
    println!("50 passes over 10 arrays of 10^5 rolls: checksum {}", check);
}
