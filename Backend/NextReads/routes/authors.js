const express=require('express');
const router=express.Router();
const auth=require('../middleware/auth');
const admin=require('../middleware/admin');
const manager=require('../middleware/manager');

const authorController=require('../controller/authors')

// router.post('/', authorController.register)

// router.post('/login', authorController.logIn )

// router.get('/me', auth,authorController.getUser)

router.post('/', [auth,admin],authorController.addAuthor)
// router.get('/authorize', [auth,admin],authorController.getRequestingUsers)
// router.delete('/:id', [auth,admin],authorController.deleteuser)
// router.get('/', [auth,admin],authorController.getUsers)
// router.post('/events/:eventId',auth,authorController.reserveSeat)
// router.get('/reservation',auth,authorController.getReservations)
// router.delete('/reservation/:eventId/:reservationId',auth,authorController.cancelReservations)
module.exports= router;