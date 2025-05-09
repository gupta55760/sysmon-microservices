// helpers/dataLoader.js

/**
 * datLoader.js
 *
 * Utility for loading test data (CSV or JSON) for Playwright GUI tests.
 *
 * Equivalent Python version: utils/data_loader.py
 * Both use the shared data files under: tests/data/
 */


const fs = require('fs');
const path = require('path');
const { parse } = require('csv-parse/sync');

function loadTestData(fileName) {
  const fullPath = path.resolve(__dirname, '../tests/data', fileName);

  if (fileName.endsWith('.json')) {
    return JSON.parse(fs.readFileSync(fullPath, 'utf-8'));
  } else if (fileName.endsWith('.csv')) {
    const csvContent = fs.readFileSync(fullPath, 'utf-8');
    const records = parse(csvContent, {
      columns: true,
      skip_empty_lines: true,
    });

    return records.map(row => ({
      ...row,
      should_pass: row.should_pass.trim().toLowerCase() === 'true',
    }));
  } else {
    throw new Error(`Unsupported file format: ${fileName}`);
  }
}

module.exports = { loadTestData };

