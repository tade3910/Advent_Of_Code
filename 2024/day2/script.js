import fs from 'fs';
import readline from 'readline';

async function validateInput() {
    const fileStream = fs.createReadStream('input.txt');
  
    // Create an interface for reading the file line by line
    const rl =  readline.createInterface({
      input: fileStream,
      crlfDelay: Infinity,
    });
    let numSafe = 0
    try {
      for await (const line of rl) {
        const numbers = line.split(/\s+/).map(Number)
        let increasing = numbers[0] < numbers[1]
        let diff = Math.abs(numbers[0] - numbers[1])
        if(diff > 3 || diff < 1) {
            continue
        }
        let addition = 1;
        for(let i = 2; i < numbers.length; i++) {
            diff = numbers[i] - numbers[i - 1]
            if(diff < 0 && increasing || diff > 0 && !increasing){
                addition = 0;
                break
            }
            diff = Math.abs(diff)
            if(diff > 3 || diff < 1) {
                addition = 0;
                break
            }
        }
        numSafe += addition
      }
    } catch (error) {
      console.error(error)
    }
    return numSafe
  }

  async function doSomeMoreShit() {
    const fileStream = fs.createReadStream('input.txt');
    // Create an interface for reading the file line by line
    const rl =  readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity,
      });
      let numSafe = 0
      try {
        for await (const line of rl) {
          const numbers = line.split(/\s+/).map(Number)
          if(isSafeWithDampener(numbers)) {
            numSafe++
          }
        }
      } catch (error) {
        console.error(error)
      }
      return numSafe
  }

  //the idea is we can either remove the current element or the previous element and validate

  function isValidSequence(sequence) {
    if(sequence.length < 2) {
        return true
    }
    const increasing = sequence[0] < sequence[1]
    for(let i = 1; i < sequence.length; i++) {
        let diff = sequence[i] - sequence[i-1]
        if(diff < 0 && increasing || diff > 0 && !increasing){
            return false
        }
        diff = Math.abs(diff)
        if(diff > 3 || diff < 1) {
            return false
        }
    }
    return true
  }

  function isSafeWithDampener(sequence) {
    if(isValidSequence(sequence)) {
        return true
    } else {
        //try removing any one index
        for(let i = 0; i < sequence.length;i++) {
            const currSequence = [...sequence.slice(0,i),...sequence.slice(i + 1)]
            if(isValidSequence(currSequence)) {
                return true
            }
        }
    }
    return false
    
  }

  console.log(await validateInput())
  console.log(await doSomeMoreShit())


    // 5 6 2 7 
  // 1 2 3 -> good
  // 5 3 6 2 -> skip prev: 3 -> changes increasing
// 1 2 5 3 -> skip curr: 5
// 1 4 2 3 -> skip prev : 4
// 5 4 1 2 3 -> no good
// 1 3 2 4 5 -> skip curr : 2
// 8 6 4 4 1 -> skip curr or prev : 4
// 1 5 4 3 -> skip prev: 1