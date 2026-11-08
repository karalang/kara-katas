// LeetCode #1500: Design a File Sharing System -- the benchmark, the same
// structure as files.kara: each chunk's owners in a sorted Vec kept by binary
// search, each user's chunks in a Vec indexed by id, free ids in a min-heap.

use std::cmp::Reverse;
use std::collections::BinaryHeap;

struct FileSharing {
    owners: Vec<Vec<i64>>,
    owned: Vec<Vec<i64>>,
    free: BinaryHeap<Reverse<i64>>,
}

fn position(v: &[i64], x: i64) -> usize {
    let (mut lo, mut hi) = (0usize, v.len());
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if v[mid] < x { lo = mid + 1; } else { hi = mid; }
    }
    lo
}

impl FileSharing {
    fn new(m: i64) -> Self {
        FileSharing { owners: vec![Vec::new(); m as usize + 1], owned: vec![Vec::new()], free: BinaryHeap::new() }
    }

    fn join(&mut self, chunks: Vec<i64>) -> i64 {
        let id = match self.free.pop() {
            Some(Reverse(id)) => id,
            None => {
                self.owned.push(Vec::new());
                self.owned.len() as i64 - 1
            }
        };
        for &c in &chunks {
            let o = &mut self.owners[c as usize];
            let at = position(o, id);
            o.insert(at, id);
        }
        self.owned[id as usize] = chunks;
        id
    }

    fn leave(&mut self, id: i64) {
        for &c in &self.owned[id as usize] {
            let o = &mut self.owners[c as usize];
            let at = position(o, id);
            o.remove(at);
        }
        self.owned[id as usize].clear();
        self.free.push(Reverse(id));
    }

    fn request(&mut self, id: i64, chunk: i64) -> Vec<i64> {
        let answer = self.owners[chunk as usize].clone();
        if !answer.is_empty() {
            let at = position(&self.owners[chunk as usize], id);
            if at == answer.len() || answer[at] != id {
                self.owners[chunk as usize].insert(at, id);
                self.owned[id as usize].push(chunk);
            }
        }
        answer
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn random_chunks(m: i64, most: i64, seed: &mut i64) -> Vec<i64> {
    let count = next_random(seed) % (most.min(m) + 1);
    let mut chunks = Vec::new();
    while (chunks.len() as i64) < count {
        let c = next_random(seed) % m + 1;
        if !chunks.contains(&c) {
            chunks.push(c);
        }
    }
    chunks
}

fn simulate(m: i64, ops: i64, most: i64, seed: &mut i64) -> (i64, i64, i64, i64) {
    let mut system = FileSharing::new(m);
    let mut live: Vec<i64> = Vec::new();
    let (mut joins, mut requests, mut owners, mut check) = (0, 0, 0, 0);
    for _ in 0..ops {
        let r = next_random(seed) % 10;
        if live.is_empty() || r < 3 {
            let id = system.join(random_chunks(m, most, seed));
            live.push(id);
            joins += 1;
            check = mix(check, id);
        } else if r < 5 {
            let at = next_random(seed) % live.len() as i64;
            system.leave(live.swap_remove(at as usize));
        } else {
            let user = live[(next_random(seed) % live.len() as i64) as usize];
            let chunk = next_random(seed) % m + 1;
            let answer = system.request(user, chunk);
            requests += 1;
            owners += answer.len() as i64;
            check = mix(check, answer.len() as i64);
            for &id in &answer {
                check = mix(check, id);
            }
        }
    }
    (joins, requests, owners, check)
}

fn batch(count: i64, most_m: i64, ops: i64, most: i64, seed: &mut i64) {
    let (mut joins, mut requests, mut owners, mut check) = (0, 0, 0, 0);
    for _ in 0..count {
        let m = next_random(seed) % most_m + 1;
        let (j, r, o, c) = simulate(m, ops, most, seed);
        joins += j;
        requests += r;
        owners += o;
        check = mix(check, c);
    }
    println!("{count} systems of up to {most_m} chunks, {ops} calls each: {joins} joins, {requests} requests, {owners} owners returned, checksum {check}");
}

fn main() {
    let mut seed = 1500;
    batch(40, 2000, 40000, 30, &mut seed);
}
