package main

import (
	"bufio"
	"log"
	"os"
)

func getMajorityValue(idx int, input *[]string) byte {
	var counter int = 0
	for row := 0; row < len(*input); row++ {
		line := (*input)[row]
		if line[idx] == byte('1') {
			counter++
		}
	}
	result := byte('0')
	if counter >= len(*input)-counter {
		result = byte('1')
	}
	return result
}

func day3(input *[]string, part02 bool) int64 {

	var result int64
	var inputCounter []int64 = nil

	for row := 0; row < len(*input); row++ {
		line := (*input)[row]

		if inputCounter == nil {
			inputCounter = make([]int64, len(line))
			for idx := 0; idx < len(inputCounter); idx++ {
				inputCounter[idx] = 0
			}
		} else if len(inputCounter) != len(line) {
			log.Fatal("input size changed")
		}
		for idx := 0; idx < len(line); idx++ {
			if line[idx] == byte('1') {
				inputCounter[idx]++
			}
		}
	}

	if !part02 {

		var gamma int = 0
		var epsilon = 0
		for idx := 0; idx < len(inputCounter); idx++ {
			v := 1 << (len(inputCounter) - idx - 1)
			if inputCounter[idx] > int64(len(*input))-inputCounter[idx] {
				gamma += v
			} else {
				epsilon += v
			}
		}

		log.Println(gamma)
		log.Println(epsilon)
		result = int64(gamma * epsilon)

	} else {

		var generatorSet []string = make([]string, len(*input))
		copy(generatorSet, *input)
		for idx := 0; idx < len(inputCounter); idx++ {
			majorityValue := getMajorityValue(idx, &generatorSet)
			var newGeneratorSet []string = make([]string, 0, len(generatorSet))
			for row := 0; row < len(generatorSet); row++ {
				line := generatorSet[row]
				if line[idx] == majorityValue {
					newGeneratorSet = append(newGeneratorSet, line)
				}
			}
			if len(newGeneratorSet) > 0 {
				generatorSet = newGeneratorSet
			}
		}
		log.Println(generatorSet)

		var scrubberSet []string = make([]string, len(*input))
		copy(scrubberSet, *input)
		for idx := 0; idx < len(inputCounter); idx++ {
			majorityValue := getMajorityValue(idx, &scrubberSet)
			var newScrubberSet []string = make([]string, 0, len(scrubberSet))
			for row := 0; row < len(scrubberSet); row++ {
				line := scrubberSet[row]
				if line[idx] != majorityValue {
					newScrubberSet = append(newScrubberSet, line)
				}
			}
			if len(newScrubberSet) > 0 {
				scrubberSet = newScrubberSet
			}
		}
		log.Println(scrubberSet)

		if len(generatorSet) == 1 && len(scrubberSet) == 1 {

			generatorKey := generatorSet[0]
			var generatorVal = 0
			for idx := 0; idx < len(generatorKey); idx++ {
				v := 1 << (len(generatorKey) - idx - 1)
				if generatorKey[idx] == byte('1') {
					generatorVal += v
				}
			}

			scrubberKey := scrubberSet[0]
			var scrubberVal = 0
			for idx := 0; idx < len(generatorKey); idx++ {
				v := 1 << (len(generatorKey) - idx - 1)
				if scrubberKey[idx] == byte('1') {
					scrubberVal += v
				}
			}

			log.Println(generatorVal)
			log.Print(scrubberVal)
			result = int64(generatorVal * scrubberVal)
		}
	}

	return result
}

func main() {

	var input []string = nil
	{
		inFile, err := os.Open("part1.txt")
		if err != nil {
			log.Fatal("cannot open input")
		} else {

			scanner := bufio.NewScanner(inFile)
			scanner.Split(bufio.ScanLines)
			for scanner.Scan() {
				input = append(input, scanner.Text())
			}
			inFile.Close()
			part1Answer := day3(&input, false)
			log.Println("part1:", part1Answer)
			part2Answer := day3(&input, true)
			log.Println("part2:", part2Answer)
		}
	}

}
