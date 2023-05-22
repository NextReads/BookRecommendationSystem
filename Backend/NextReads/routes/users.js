const express=require('express');
const router=express.Router();
const auth=require('../middleware/auth');
const admin=require('../middleware/admin');
const manager=require('../middleware/manager');

const userController=require('../controller/users')

router.post('/', userController.register)

router.post('/login', userController.logIn )

router.get('/me', auth,userController.getUser)

// router.put('/authorize', [auth,admin],userController.authorize)
// router.get('/authorize', [auth,admin],userController.getRequestingUsers)
// router.delete('/:id', [auth,admin],userController.deleteuser)
router.get('/', [auth,admin],userController.getUsers)
router.get('/readbooks',[auth],userController.getReadBooks)
router.get('/wanttoread',[auth],userController.getWantToRead)
router.get('/ratedbooks',[auth],userController.getRatedBooks)
router.post('/:bookId/wanttoread',[auth],userController.addToWantToRead)
router.post('/:bookId/toreadnext',[auth],userController.toReadNext)
router.get('/toreadnext',[auth],userController.getToReadNext)
router.get('/searchInRead',[auth],userController.searchInRead)
router.get('/searchInTbr',[auth],userController.searchInTbr)

// router.post('/events/:eventId',auth,userController.reserveSeat)
// router.get('/reservation',auth,userController.getReservations)
// router.delete('/reservation/:eventId/:reservationId',auth,userController.cancelReservations)
module.exports= router;