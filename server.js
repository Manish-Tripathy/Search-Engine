const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = 3000;
const trie=require('./trie');

app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

const codes = fs.readFileSync('./data_codechef/codechef_code.txt', 'utf-8').split('\n');
const names = fs.readFileSync('./data_codechef/codechef_name.txt', 'utf-8').split('\n');
const diffs = fs.readFileSync('./data_codechef/codechef_difficulty.txt', 'utf-8').split('\n');

const loadProblems = () => {

  return codes.map((code, i) => ({
    code: code.trim(),
    name: (names[i] || '').trim(),
    difficulty: (diffs[i] || '').trim()
  }));
};


const problems = loadProblems();

app.get('/', (req, res) => {
  res.render('index', { query: '', initial: problems.slice(0, 100) });
});

app.get('/problem/:id', (req, res) => {
   const id = req.params.id;
   const filePath = path.join(__dirname, 'codechef_problems_txt', `${id}.txt`);
 
   fs.readFile(filePath, 'utf8', (err, data) => {
     if (err) {
       return res.status(404).send('Problem not found');
     }
 
     res.render('problem', {
       title: `Problem ${id}`,
       code: id,
       body: data
     });
   });
 });
 //trie check
 app.get('/idf/:word', (req, res) => {
   const word = req.params.word.toLowerCase();
   const result = trie.search(word);
   if (!result) return res.status(404).send('Word not found');
   res.json(result);
 });


//  app.post('/search', (req, res) => {
//    const query = req.body.query;
//    if (!query) return res.status(400).send('Empty query');
 
//    const words = query.trim().toLowerCase().split(/\s+/);
//    const totalWords = words.length;
 
//    const wordFreq = {};
//    words.forEach(word => {
//      wordFreq[word] = (wordFreq[word] || 0) + 1;
//    });
 
//    const resultArray = [];
 
//    for (const word in wordFreq) {
//      const tf = wordFreq[word] / totalWords;
//      const searchResult = trie.search(word);
//      if (searchResult) {
//        const { row, idf } = searchResult;
//        resultArray.push({ row, score: tf * idf });
//      }
//    }
 
//    // Sort descending by score
//    resultArray.sort((a, b) => a.row-b.row);
 
//    res.json(resultArray);
//  });

app.post('/search', (req, res) => {
   const query = req.body.query;
   if (!query) return res.status(400).send('Empty query');
 
   const words = query.trim().toLowerCase().split(/\s+/);
   const totalWords = words.length;
 
   const wordFreq = {};
   words.forEach(word => {
     wordFreq[word] = (wordFreq[word] || 0) + 1;
   });
 
   const resultArray = []; // This is the query vector: { row, score }
   const vector1 = {};     // For fast lookup
 
   for (const word in wordFreq) {
     const tf = wordFreq[word] / totalWords;
     const searchResult = trie.search(word);
     if (searchResult) {
       const { row, idf } = searchResult;
       const score = tf * idf;
       resultArray.push({ row, score });
       vector1[row] = score;
     }
   }
 
   const tfidfLines = fs.readFileSync('./data_codechef/TFIDF.txt', 'utf-8').split('\n');
 
   const similarities = tfidfLines.map((line, index) => {
     const tokens = line.trim().split(/\s+/);
     const vector2 = {};
 
     for (let i = 0; i < tokens.length; i += 2) {
       const r = parseInt(tokens[i]);
       const v = parseFloat(tokens[i + 1]);
       if (!isNaN(r) && !isNaN(v)) vector2[r] = v;
     }
 
     // Dot product
     let dot = 0;
     for (const r in vector1) {
       if (vector2[r]) {
         dot += vector1[r] * vector2[r];
       }
     }
 
     // Magnitudes
     const mag1 = Math.sqrt(Object.values(vector1).reduce((sum, val) => sum + val * val, 0));
     const mag2 = Math.sqrt(Object.values(vector2).reduce((sum, val) => sum + val * val, 0));
 
     const sim = (mag1 && mag2) ? dot / (mag1 * mag2) : 0;
     return { row: index, sim };
   });
 
   // Sort by similarity score
   const top = similarities.sort((a, b) => b.sim - a.sim).slice(0, 10);
 
   const finalResults = top.map(({ row, sim }) => ({
     code: codes[row],
     name: names[row],
     difficulty: diffs[row],
   //   score: sim.toFixed(4)
   }));
 
   res.render('results', { query, results: finalResults });
 });
 

app.get('/api/problems', (req, res) => {
  const offset = parseInt(req.query.offset) || 0;
  const limit = parseInt(req.query.limit) || 100;
  const slice = problems.slice(offset, offset + limit);
  res.json(slice);
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
