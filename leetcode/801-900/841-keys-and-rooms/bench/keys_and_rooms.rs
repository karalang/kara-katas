// Benchmark for #841: Keys and Rooms -- the ★ arm (a stack of rooms to open).
//
// Mirrors keys_and_rooms.kara: room 0 is open; every room opened is put
// on a stack, and a room taken off the stack gives up its keys, each key
// to a room not yet opened opening it.

fn can_visit_all_rooms(rooms: &[Vec<i64>]) -> bool {
    let n = rooms.len() as i64;
    let mut opened: Vec<bool> = vec![false; n as usize];
    opened[0] = true;
    let mut count = 1;
    let mut stack: Vec<i64> = vec![0];
    while let Some(room) = stack.pop() {
        for k in 0..rooms[room as usize].len() {
            let key = rooms[room as usize][k];
            if !opened[key as usize] {
                opened[key as usize] = true;
                count += 1;
                stack.push(key);
            }
        }
    }
    count == n
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 64 cases drawn once, each LeetCode's most rooms, 1000: case g puts
    // 2000 keys, each to a random room, in random rooms, no room holding
    // two keys to the same room; when g is even it then threads the
    // rooms in a shuffled order, each holding a key to the next, so that
    // every room can be visited. Each round asks the next case.
    let count: i64 = 64;
    let rounds: i64 = 36000;
    let n: i64 = 1000;
    let mut seed: i64 = 841;
    let mut cases: Vec<Vec<Vec<i64>>> = Vec::new();
    for g in 0..count {
        let mut rooms: Vec<Vec<i64>> = vec![Vec::new(); n as usize];
        for _ in 0..2000 {
            let from = (next_random(&mut seed) % n) as usize;
            let to = next_random(&mut seed) % n;
            if !rooms[from].contains(&to) {
                rooms[from].push(to);
            }
        }
        if g % 2 == 0 {
            let mut order: Vec<i64> = (0..n).collect();
            for i in (2..n).rev() {
                let j = 1 + next_random(&mut seed) % i;
                order.swap(i as usize, j as usize);
            }
            for i in 0..(n - 1) as usize {
                if !rooms[order[i] as usize].contains(&order[i + 1]) {
                    let next = order[i + 1];
                    rooms[order[i] as usize].push(next);
                }
            }
        }
        cases.push(rooms);
    }
    let mut yes: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let all = can_visit_all_rooms(&cases[(round % count) as usize]);
        if all {
            yes += 1;
        }
        checksum = (checksum * 31 + if all { round % 1000 } else { 7 }) % 1000000007;
    }
    println!("{rounds} rounds of {count} cases: {yes} with every room visited, checksum {checksum}");
}
