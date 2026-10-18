// LeetCode 752 — Open the Lock, bench: the ★ arm (breadth-first over
// numbers) against 500 dead ends that keep changing. Mirrors open_lock.kara.
use std::collections::VecDeque;

fn open_lock(deadends: &[String], target: &str) -> i64 {
    let mut blocked = vec![false; 10000];
    for d in deadends {
        blocked[d.parse::<usize>().unwrap()] = true;
    }
    let goal: usize = target.parse().unwrap();
    if blocked[0] {
        return -1;
    }
    let mut dist = vec![-1i64; 10000];
    dist[0] = 0;
    let mut queue = VecDeque::new();
    queue.push_back(0usize);
    while let Some(at) = queue.pop_front() {
        if at == goal {
            return dist[at];
        }
        let mut place = 1;
        for _ in 0..4 {
            let digit = at / place % 10;
            for step in [1, 9] {
                let next = at - digit * place + (digit + step) % 10 * place;
                if !blocked[next] && dist[next] == -1 {
                    dist[next] = dist[at] + 1;
                    queue.push_back(next);
                }
            }
            place *= 10;
        }
    }
    -1
}

struct Rng(i64);
impl Rng {
    fn next(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn four(x: i64) -> String {
    format!("{}{}{}{}", x / 1000, x / 100 % 10, x / 10 % 10, x % 10)
}

fn main() {
    let rounds = 3000;
    let mut rng = Rng(752);
    let mut deadends: Vec<String> = (0..500).map(|_| four(1 + rng.next() % 9999)).collect();
    let mut total = 0i64;
    let mut stuck = 0i64;
    for _ in 0..rounds {
        for _ in 0..5 {
            let i = (rng.next() % 500) as usize;
            deadends[i] = four(1 + rng.next() % 9999);
        }
        let target = four(rng.next() % 10000);
        let turns = open_lock(&deadends, &target);
        if turns == -1 {
            stuck += 1;
        } else {
            total += turns;
        }
    }
    println!("{} locks with 500 dead ends: {} cannot open, the rest take {} turns in all", rounds, stuck, total);
}
