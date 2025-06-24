const mongoose = require('mongoose');

const ProblemSchema = new mongoose.Schema({
  code: { type: String, required: true, unique: true },
  name: String,
  difficulty: Number,
  statement: String
});

module.exports = mongoose.model('Problem', ProblemSchema);
