import fs from 'fs';
import readline from 'readline';

  async function getLines() {
    const fileStream = fs.createReadStream('input.txt');
  
    // Create an interface for reading the file line by line
    const rl =  readline.createInterface({
      input: fileStream,
      crlfDelay: Infinity,
    });
    try {
      const lines = []
      for await (const line of rl) {
        lines.push(line)
      }
      return lines
    } catch (error) {
      console.error(error)
    }
  }

  function countHorizontal(row,col,lines,count) {
    const line = lines[row]
    count = line.substring(col,col + 4) == "XMAS" ? count + 1 : count
    count = line.substring(col -3, col + 1) == "SAMX" ? count + 1 : count
    return count
  }

  function countDown(row,col,lines,count) {
    let downString = ""
    if(row + 3 < lines.length) {
      for(let i = 0; i < 4;i++) {
        const line = lines[row + i]
        if(col >= line.length) {
          break
        }
        downString += line.charAt(col)
      }
    }
    
    return downString == "XMAS" ? count + 1 : count
  }

  function countUp(row,col,lines,count) {
    let upString = ""
    if(row - 3 >= 0) {
      for(let i = 0; i < 4;i++) {
        const line = lines[row - i]
        if(col >= line.length) {
          break
        }
        upString += line.charAt(col)
      }
    }
    
    return upString == "XMAS" ? count + 1 : count
  }

  function countDiagonal(row,col,lines,count) {
    let downRight = ""
    let downLeft = ""
    if(row + 3 < lines.length) {
      for(let i = 0; i < 4;i++) {
        const line = lines[row + i]
        let rightCol = col + i
        let leftCol = col - i
        if(rightCol < line.length) {
          downRight += line.charAt(rightCol)
        }
        if(leftCol >= 0) {
          downLeft += line.charAt(leftCol)
        }
      }
    }
    let upRight = ""
    let upLeft = ""
    if(row - 3 >= 0) {
      for(let i = 0; i < 4;i++) {
        const line = lines[row - i]
        let rightCol = col + i
        let leftCol = col - i
        if(rightCol < line.length) {
          upRight += line.charAt(rightCol)
        }
        if(leftCol >= 0) {
          upLeft += line.charAt(leftCol)
        }
      }
    }
    const strings = [downRight,downLeft,upRight,upLeft]
    for(let string of strings) {
      count = string == "XMAS" ? count + 1: count
    }
    return count
  }

  

  function countXMAS(lines) {
    let count = 0;
    for(let row = 0; row < lines.length;row++) {
      const line = lines[row]
      for(let col = 0; col < line.length; col++) {
        const cur = line.charAt(col)
        if(cur == "X") {
          count = countDiagonal(row,col,lines,count)
          count = countDown(row,col,lines,count)
          count = countUp(row,col,lines,count)
          count = countHorizontal(row,col,lines,count)
        }
      }
    }
    return count;
  }


const l = await getLines()
console.log(countXMAS(l))






//Need to start on A
/**
 * M - S
 * - A - found
 * M - S
 */

/**
 * M - M
 * - A -  found
 * S - S
 */

/**
 * S - M
 * - A - found 
 * S - M
 */

/**
 * S - S
 * - A - found
 * M - M
 */


function poop(row,col,lines,count,topLeft,topRight,bottomLeft,bottomRight) {
const stinkyPoop = (ds,index,shift) => {return index - shift >= 0 && index + shift < ds.length}

  if(!stinkyPoop(lines,row,1)) {
    return count
  }
  const top = lines[row - 1]
  const bottom = lines[row + 1]
  if(!stinkyPoop(top,col,1) || !stinkyPoop(bottom,col,1)) {
    return count
  }
  const tl = top.charAt(col - 1)
  const tr = top.charAt(col + 1)
  const bl = bottom.charAt(col - 1)
  const br = bottom.charAt(col + 1)
  return topLeft == tl && tr == topRight && bl == bottomLeft && br == bottomRight ? count + 1 : count
}

function poopOnMe(lines) {
  let count = 0;
  for(let row = 0; row < lines.length;row++) {
    const line = lines[row]
    for(let col = 0; col < line.length; col++) {
      const cur = line.charAt(col)
      if(cur == "A") {
        count = poop(row,col,lines,count,'M','S','M','S') 
        count = poop(row,col,lines,count,'M','M','S','S') 
        count = poop(row,col,lines,count,'S','M','S','M') 
        count = poop(row,col,lines,count,'S','S','M','M') 
      }
    }
  }
  return count;
}
console.log(poopOnMe(l))