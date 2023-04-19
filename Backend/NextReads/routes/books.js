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
router.post('/:id/review', auth,bookController.addReview);
// router.put('/events/info/:id',[auth,manager],bookController.editEvent);
// router.get('/:id',bookController.getEvent);
// router.get('/events/:bookId',bookController.getEvents);
// router.get('/events/seats/:eventId',bookController.getSeats);
module.exports = router;