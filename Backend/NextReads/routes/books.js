const express = require('express');
const auth = require('../middleware/auth');
const admin = require('../middleware/admin');
const manager = require('../middleware/manager');
const bookController = require('../controller/books');

const router = express.Router();

router.post('/', [auth, manager], bookController.addBook);

// router.get('/', bookController.getbooks);
// router.get('/api/courses/:id', (req, res) => {
//     res.send(req.params.id);
// });
router.post('/:id/review', [auth],auth,bookController.addReview);
router.post('/coldstart', [auth],bookController.addRatings);
router.post('/:id/rating', [auth],bookController.addRating);
router.get('/recommend', [auth],bookController.Recommender);
router.get('/getbooks',bookController.getBooks);
router.get('/book/:id',bookController.getBook);
// add search route handler where search is dony by query string of the form:
// /api/books/search?search=bookTitle&pageNumber=pageNumber
// the search should be case insensitive
// the search should be a substring search
// the search should be a partial search
// the search should be a fuzzy search
// the search should be a full text search
router.get('/search',bookController.searchBooks);
router.get('/genre',bookController.getByGenre);
// router.get('/search',bookController.searchBooks);

// router.put('/events/info/:id',[auth,manager],bookController.editEvent);
// router.get('/:id',bookController.getEvent);
// router.get('/events/:bookId',bookController.getEvents);
// router.get('/events/seats/:eventId',bookController.getSeats);
module.exports = router;