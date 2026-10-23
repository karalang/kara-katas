// LeetCode #874 bench: Rust mirror of robot_sim.kara (the ★ arm, a
// HashSet of obstacles) on the same 600 walks.

use std::collections::HashSet;

fn robot_sim(commands: &[i64], obstacles: &[Vec<i64>]) -> i64 {
    let mut blocked: HashSet<i64> = HashSet::new();
    for o in obstacles {
        blocked.insert(square(o[0], o[1]));
    }
    let dx = [0, 1, 0, -1];
    let dy = [1, 0, -1, 0];
    let mut facing = 0;
    let (mut x, mut y) = (0i64, 0i64);
    let mut best = 0;
    for &c in commands {
        if c == -2 {
            facing = (facing + 3) % 4;
        } else if c == -1 {
            facing = (facing + 1) % 4;
        } else {
            for _ in 0..c {
                let nx = x + dx[facing];
                let ny = y + dy[facing];
                if blocked.contains(&square(nx, ny)) {
                    break;
                }
                x = nx;
                y = ny;
                best = best.max(x * x + y * y);
            }
        }
    }
    best
}

fn square(x: i64, y: i64) -> i64 {
    (x + 200000) * 400001 + (y + 200000)
}

struct Rng(i64);

impl Rng {
    fn next(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn random_commands(rng: &mut Rng, n: usize, turns: i64) -> Vec<i64> {
    let mut commands = Vec::with_capacity(n);
    for _ in 0..n {
        if rng.next() % turns == 0 {
            commands.push(-1 - rng.next() % 2);
        } else {
            commands.push(rng.next() % 9 + 1);
        }
    }
    commands
}

fn random_obstacles(rng: &mut Rng, n: usize, reach: i64) -> Vec<Vec<i64>> {
    let mut obstacles = Vec::with_capacity(n);
    for _ in 0..n {
        let x = rng.next() % (2 * reach + 1) - reach;
        let y = rng.next() % (2 * reach + 1) - reach;
        obstacles.push(vec![x, y]);
    }
    obstacles
}

fn main() {
    let mut rng = Rng(874);
    let mut command_lists = Vec::new();
    let mut obstacle_lists = Vec::new();
    for k in 0..20 {
        command_lists.push(random_commands(&mut rng, 10000, 2 + k % 3));
        obstacle_lists.push(random_obstacles(&mut rng, 10000, 100 + 10 * k));
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for k in 0..600usize {
        let answer = robot_sim(&command_lists[k % 20], &obstacle_lists[(k * 7 + k / 20) % 20]);
        total += answer;
        check = (check * 131 + answer) % 1000000007;
    }
    println!("600 walks of 10000 commands among 10000 obstacles: distances sum to {}, checksum {}", total, check);
}
