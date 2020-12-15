use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead, Error};

const AOCDEBUG: bool = false;

type AOCResult = std::result::Result<(), Error>;

#[derive(Debug)]
pub struct AOCGame {
    memory: HashMap<i32, i32>,
    turn: i32,
}

impl AOCGame {
    pub fn new() -> AOCGame {
        AOCGame {
            memory: HashMap::new(),
            turn: 0,
        }
    }
    pub fn next(&mut self, n: i32) -> i32 {
        self.turn += 1;
        let mut rval = 0;
        match self.memory.get(&n) {
            Some(v) => {
                rval = self.turn - *v;
            }
            None => {}
        }
        self.memory.insert(n, self.turn);
        rval
    }
}

struct AOCProcessor {
    source: String,
    seeds: Vec<i32>,
}

impl AOCProcessor {
    pub fn new(source: String) -> AOCProcessor {
        AOCProcessor {
            source,
            seeds: Vec::new(),
        }
    }

    pub fn process(&mut self) -> AOCResult {
        self.initialize();

        let _ = match File::open(&self.source) {
            Ok(file) => {
                for line in io::BufReader::new(file).lines() {
                    if let Ok(line) = line {
                        self.process_line(&line[..]);
                    }
                }
            }
            Err(error) => return Err(error),
        };

        self.finalize();

        Ok(())
    }

    pub fn initialize(&mut self) {
        self.seeds.clear();
    }

    pub fn finalize(&mut self) {
        if AOCDEBUG {
            println!("{:?}", self.seeds);
        }

        let result_a = self.finalize_n(2020);
        println!("result_a:{}", result_a);

        let result_b = self.finalize_n(30000000);
        println!("result_b:{}", result_b);
    }

    fn process_line(&mut self, line: &str) {
        if line.len() > 0 {
            for token in line.split(',') {
                self.seeds.push(token.parse::<i32>().unwrap());
            }
        }
    }

    fn finalize_n(&mut self, n: i32) -> i32 {
        let mut game = AOCGame::new();

        let mut turn = 1;
        let mut pval = 0;
        for v in &self.seeds {
            pval = game.next(*v);
            turn += 1;
        }
        while turn < n {
            turn += 1;
            pval = game.next(pval);
        }
        pval
    }
}

fn main() {
    let mut processor = AOCProcessor::new(String::from("input.txt"));
    match processor.process() {
        Ok(()) => {
            println!("DONE");
        }
        Err(error) => {
            panic!("{:#?}", error);
        }
    }
}
