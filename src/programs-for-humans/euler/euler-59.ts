import { readFile } from 'fs/promises';

function gibberishScore(text: number[]): number {
  let gibberishCount = 0;
  const isReadable = (c: number) => c >= 'a'.charCodeAt(0) && c <= 'z'.charCodeAt(0); 

  for (const c of text) {
    if (!isReadable(c)) gibberishCount++;
  }
  return gibberishCount / text.length;
}

async function loadInput(filePath: string): Promise<number[]> {
  try {
    const data = await readFile(filePath, 'utf-8');
    return data.split(",").map((code: string, _) => parseInt(code)); 
  } catch (error) {
    console.error('Error reading file:', error);
    throw error;
  }
}

function decrypt(cipher: number[], key: number[]): number[] {
  if (cipher.length % key.length != 0) {
    throw Error("cipher must be multiple of key length");
  }

  const keyLength = key.length;
  return cipher.map((c, i) => c ^ key[i % keyLength]);
}

function allKeys(): number[][] {
  let result = [];
  const a = "a".charCodeAt(0);
  const z = "z".charCodeAt(0);

  for (let i = a; i <= z; i++) {
    for (let j = a; j <= z; j++) {
      for (let k = a; k <= z; k++) {
        result.push([i, j, k]);
      }
    }
  } 
  return result;
}

async function problem59() {
  const cipher = await loadInput("src/code/data/euler-59.txt");
  let bestGuess: {
    key: number[],
    plain: number[],
    score: number
  } = {
    key: [],
    plain: [],
    score: 1
  };

  for (let k of allKeys()) {
    const plain = decrypt(cipher, k);
    const score = gibberishScore(plain);
    if (score < bestGuess.score) {
      bestGuess.key = k;
      bestGuess.plain = plain;
      bestGuess.score = score;
    }
  }
  console.log(bestGuess.plain.reduce((total, x) => total + x, 0));
}

export {
  gibberishScore,
  decrypt
}

problem59();