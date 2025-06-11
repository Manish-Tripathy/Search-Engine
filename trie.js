const fs = require('fs');
const path = require('path');

class TrieNode {
  constructor() {
    this.children = {};
    this.row = null;
    this.idf = null;
  }
}

class Trie {
  constructor() {
    this.root = new TrieNode();
  }

  insert(word, row, idf) {
    let node = this.root;
    for (const char of word) {
      if (!node.children[char]) node.children[char] = new TrieNode();
      node = node.children[char];
    }
    node.row = row;
    node.idf = idf;
  }

  search(word) {
    let node = this.root;
    for (const char of word) {
      if (!node.children[char]) return null;
      node = node.children[char];
    }
    return node.row !== null ? { row: node.row, idf: node.idf } : null;
  }
}

const trie = new Trie();

// File paths
const wordFilePath = path.join(__dirname, '/data/codechef_lexicographical_word.txt');
const idfFilePath = path.join(__dirname, '/data/codechef_idf.txt');

// Load files
const words = fs.readFileSync(wordFilePath, 'utf-8').split('\n');
const idfs = fs.readFileSync(idfFilePath, 'utf-8').split('\n').map(parseFloat);

// Build Trie
words.forEach((word, index) => {
  const cleanWord = word.trim();
  const idf = idfs[index];
  if (cleanWord && !isNaN(idf)) {
    trie.insert(cleanWord, index, idf);
  }
});

module.exports = trie;
