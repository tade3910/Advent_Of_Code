import fs from 'fs';
import readline from 'readline';


async function doShit() {
    const firstNumbers = [];
    const secondNumbers = [];
    await processLists(firstNumbers,secondNumbers)
    sortAscending(firstNumbers)
    sortAscending(secondNumbers)
    return getTotalDistance(firstNumbers,secondNumbers)
}

const getTotalDistance = (firstNumbers,secondNumbers) => {
    let distance = 0;
    for(let i = 0; i < firstNumbers.length;i++) {
        let min = firstNumbers[i]
        let max = secondNumbers[i]
        if (min > max) {
            min = secondNumbers[i]
            max = firstNumbers[i]
        }
        let diff = max - min
        distance += diff
    }
    return distance
}

const sortAscending = list => {
    list.sort((a, b) => a - b)
}

async function getMaSecondStar() {
    const firstNumbers = {};
    const secondNumbers = {};
    await processMaps(firstNumbers,secondNumbers)
    let similarity = 0;
    for(const key of Object.keys(firstNumbers)) {
        if(secondNumbers[key]) {
            console.log(key)
            let curr = key * secondNumbers[key]
            curr *= firstNumbers[key]
            similarity += curr
        }
    }
    return similarity
}

async function processMaps(firstNumbers,secondNumbers) {
    const fileStream = fs.createReadStream('input.txt');
  
    // Create an interface for reading the file line by line
    const rl = readline.createInterface({
      input: fileStream,
      crlfDelay: Infinity,
    });
  
    try {
      for await (const line of rl) {
        const numbers = line.split(/\s+/)
        const firstNumber = numbers[0]
        const secondNumber = numbers[1]
        if(firstNumbers[firstNumber]) {
            firstNumbers[firstNumber]++
        } else {
            firstNumbers[firstNumber] = 1
        }

        if(secondNumbers[secondNumber]) {
            secondNumbers[secondNumber]++
        } else {
            secondNumbers[secondNumber] = 1
        }
      }
    } catch (error) {
      console.error(error)
    }
  }

async function processLists(firstNumbers,secondNumbers) {
  const fileStream = fs.createReadStream('test.txt');

  // Create an interface for reading the file line by line
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity,
  });

  

  try {
    for await (const line of rl) {
      const numbers = line.split(/\s+/)
      firstNumbers.push(numbers[0]);
      secondNumbers.push(numbers[1]);
    }
  } catch (error) {
    console.error(error)
  }
}

// Call the function
// console.log(await doShit())
console.log(await getMaSecondStar())

