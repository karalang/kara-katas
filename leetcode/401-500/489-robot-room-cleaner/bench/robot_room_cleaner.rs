// Benchmark for #489: Rust mirror of the ★ arm (backtracking); see
// robot_room_cleaner.kara.
use std::collections::HashSet;

const STEP: [(i64, i64); 4] = [(-1, 0), (0, 1), (1, 0), (0, -1)];

struct Robot {
    room: Vec<Vec<i64>>,
    row: i64,
    col: i64,
    facing: usize,
    cleaned: Vec<Vec<i64>>,
    calls: i64,
    budget: i64,
}

impl Robot {
    fn new(room: Vec<Vec<i64>>, row: i64, col: i64, facing: usize) -> Robot {
        let cleaned = room.iter().map(|line| vec![0; line.len()]).collect();
        let cells = (room.len() * room[0].len()) as i64;
        Robot { room, row, col, facing, cleaned, calls: 0, budget: 16 * cells * cells + 1000 }
    }

    fn forward(&mut self) -> bool {
        self.calls += 1;
        if self.calls > self.budget {
            return false;
        }
        let (dr, dc) = STEP[self.facing];
        let (r, c) = (self.row + dr, self.col + dc);
        if r < 0 || r >= self.room.len() as i64 || c < 0 || c >= self.room[0].len() as i64 || self.room[r as usize][c as usize] == 0 {
            return false;
        }
        self.row = r;
        self.col = c;
        true
    }

    fn turn_right(&mut self) {
        self.calls += 1;
        if self.calls <= self.budget {
            self.facing = (self.facing + 1) % 4;
        }
    }

    fn clean(&mut self) {
        self.calls += 1;
        if self.calls <= self.budget {
            self.cleaned[self.row as usize][self.col as usize] += 1;
        }
    }
}

fn explore(robot: &mut Robot, row: i64, col: i64, facing: usize, visited: &mut HashSet<(i64, i64)>) {
    visited.insert((row, col));
    robot.clean();
    let mut d = facing;
    for _ in 0..4 {
        let next = (row + STEP[d].0, col + STEP[d].1);
        if !visited.contains(&next) && robot.forward() {
            explore(robot, next.0, next.1, d, visited);
            robot.turn_right();
            robot.turn_right();
            robot.forward();
            robot.turn_right();
            robot.turn_right();
        }
        robot.turn_right();
        d = (d + 1) % 4;
    }
}

fn clean_room(robot: &mut Robot) {
    let mut visited = HashSet::new();
    explore(robot, 0, 0, 0, &mut visited);
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn run() {
    let mut rooms: Vec<Vec<Vec<i64>>> = Vec::new();
    let mut starts: Vec<(i64, i64)> = Vec::new();
    let mut seed: i64 = 489;
    for _ in 0..300 {
        let mut room: Vec<Vec<i64>> = Vec::new();
        for _ in 0..100 {
            let mut line: Vec<i64> = Vec::new();
            for _ in 0..100 {
                line.push(if next_random(&mut seed) % 4 == 0 { 0 } else { 1 });
            }
            room.push(line);
        }
        let row = next_random(&mut seed) % 100;
        let col = next_random(&mut seed) % 100;
        room[row as usize][col as usize] = 1;
        rooms.push(room);
        starts.push((row, col));
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for k in 0..rooms.len() {
        let (row, col) = starts[k];
        let mut robot = Robot::new(rooms[k].clone(), row, col, 0);
        clean_room(&mut robot);
        let mut cleaned = 0;
        for r in 0..100 {
            for c in 0..100 {
                if robot.cleaned[r][c] > 0 {
                    cleaned += 1;
                    checksum = (checksum * 31 + (r * 100 + c) as i64) % 1000000007;
                }
            }
        }
        total += cleaned;
        checksum = (checksum * 31 + robot.calls) % 1000000007;
    }
    println!("300 rooms of 100 by 100: {total} cells cleaned, checksum {checksum}");
}

fn main() {
    // The search recurses once per cell, up to 10,000 deep.
    std::thread::Builder::new().stack_size(512 << 20).spawn(run).unwrap().join().unwrap();
}
