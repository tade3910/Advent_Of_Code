import fs from 'fs';
import readline from 'readline';

const isDigit = (char) => char >= '0' && char <= '9';

function trymul(line,i,sum) {
  if(line.charAt(i++) === "m") {
    if(i < line.length && line.charAt(i) === "u") {
      i++
      if(i < line.length && line.charAt(i) === 'l') {
        i++
        if(i < line.length && line.charAt(i) === '(') {
          i++
          let firstNum = ""
          while(i < line.length && line.charAt(i) != ',') {
            if(!isDigit(line.charAt(i))) {
              break
            }
            firstNum += line.charAt(i++)
          }
          if(line.charAt(i) == ',') {
            i++
            let secondNum = ""
            while(i < line.length && line.charAt(i) != ')') {
              if(!isDigit(line.charAt(i))) {
                break
              }
              secondNum += line.charAt(i++)
            }
            if(line.charAt(i) == ')') {
              i++
              sum += (firstNum * secondNum)
            }
          }
        }
      }
    }
  }
  return [i,sum]
}

function getMul(line){
  let sum = 0
  let i = 0;
  while(i < line.length) {
    let result = trymul(line,i,sum)
    i = result[0]
    sum = result[1]

  }
  return sum
}

async function doMul() {
    const fileStream = fs.createReadStream('input.txt');
  
    // Create an interface for reading the file line by line
    const rl =  readline.createInterface({
      input: fileStream,
      crlfDelay: Infinity,
    });
    try {
      let sum = 0
      for await (const line of rl) {
        sum += getMul(line)
      }
      return sum
    } catch (error) {
      console.error(error)
    }
  }

  async function bombaToMe() {
    const fileStream = fs.createReadStream('input.txt');
  
    // Create an interface for reading the file line by line
    const rl =  readline.createInterface({
      input: fileStream,
      crlfDelay: Infinity,
    });
    try {
      let sum = 0
      let disabled = false
      for await (const line of rl) {
        let result = bomba(line,disabled)
        sum += result[0]
        disabled = result[1]
      }
      return sum
    } catch (error) {
      console.error(error)
    }
  }


  function getNextDo(line,i) {
    while(i < line.length) {
      if(line.charAt(i++) === 'd') {
        if(i < line.length && line.charAt(i) === 'o') {
          i++
          if(i < line.length && line.charAt(i) === '(') {
            i++
            if(i < line.length &&line.charAt(i) === ')') {
              return i + 1
            }
          }
        }
      }
    }
    return i
  }



  function bomba(line,disabled){
    let sum = 0
    let i = 0;

    while(i < line.length) {
      if(disabled || (i > 6 && line.substring(i - 7,i) === "don't()")) {
        i = getNextDo(line,i)
        if(i >= line.length) {
          return [sum,true]
        }
      }
      disabled = false
      // let oldSum = sum
      let result = trymul(line,i,sum)
      i = result[0]
      sum = result[1]
    }
    return [sum,false]
  }



console.log(await doMul())
console.log(await bombaToMe())