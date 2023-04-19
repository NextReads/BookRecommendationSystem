const express = require('express');
const router = express.Router();

const books = require('./books');
const users = require('./users');
const authors = require('./authors');

router.use('/books', books);
router.use('/users', users);
router.use('/authors', authors);

module.exports = router;