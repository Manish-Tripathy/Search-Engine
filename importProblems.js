const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');
const Problem = require('./models/Problem');

URI='mongodb+srv://manishtripathy2004:g34bLilXvxz1ngPr@cluster0.q794v71.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
// connect to MongoDB Atlas
mongoose.connect(URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(() => {
  console.log('✅ Connected to MongoDB Atlas');
  importProblems();
}).catch(err => {
  console.error('❌ MongoDB connection error:', err);
});

async function importProblems() {
  const codes = fs.readFileSync('./data_codechef/codechef_code.txt', 'utf-8').split('\n');
  const names = fs.readFileSync('./data_codechef/codechef_name.txt', 'utf-8').split('\n');
  const diffs = fs.readFileSync('./data_codechef/codechef_difficulty.txt', 'utf-8').split('\n');

  for (let i = 0; i < codes.length; i++) {
    const code = codes[i].trim();
    const name = (names[i] || '').trim();
    const difficulty = parseInt(diffs[i] || 0);
    const filePath = path.join(__dirname, 'codechef_problems_txt', `${code}.txt`);

    if (!code) continue; // skip empty lines

    let statement = '';
    if (fs.existsSync(filePath)) {
      statement = fs.readFileSync(filePath, 'utf-8');
    }

    try {
      await Problem.updateOne(
        { code },
        { $set: { name, difficulty, statement } },
        { upsert: true }
      );
      console.log(`✅ Inserted/Updated: ${code}`);
    } catch (err) {
      console.error(`❌ Error inserting ${code}:`, err.message);
    }
  }

  mongoose.disconnect();
}
