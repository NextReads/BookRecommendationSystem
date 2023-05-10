const {validateBook,  Book,validateReview,Review}=require('../models/book')
const {Author,validateAuthor}=require('../models/author')
const {User, Read,validateRating}=require('../models/user')
const _=require('lodash');
// const spawn = require("child_process").spawn;
// const https = require('http');
// const axios = require('axios');
// const { json } = require('body-parser');
// const { response } = require('express');
const fetch = require('node-fetch')





module.exports.addBook= async (req, res, next) => {
    // documentation
    // this function is used to add a new book to the database
    // req.body should contain the following fields
    // title
    // imageUrl
    // the function will return 201 if the book is added successfully
    // the function will return 400 if the book already exists
    // the function will return 400 if the request body is not valid
    // the function will return 500 if there is an internal server error
    // the function will return 400 if the author does not exist


    let { error } = validateBook(_.pick(req.body,['title','imageUrl']));
    if (error) return res.status(400).send(error.details[0].message);
    let { error1 } = validateAuthor(_.pick(req.body,['firstNAme','middleName','lastName']));
    if (error1) return res.status(400).send(error.details[0].message);

    let author = await Author.findOne({$and: [{ firstName: req.body.firstName }, {middleName: req.body.middleName},{ lastName: req.body.lastName }]}) 
    if (!author){
        return res.status(400).send('Author does not exist, please add the Author first');
    }

    let book = await Book.findOne({"title":req.body.title, 'Author':Author._id});
    if (book){return res.status(400).send('Book already exists by the same Author');}
    book=new Book({
        title:req.body.title,
        imageUrl:req.body.imageUrl,
        Author: author._id,
        isbn:req.body.isbn,
        genre:req.body.genre
    })
    author.books.push(book._id);
    
    try {
        await author.save();
        await book.save();
        return res.status(201).send('Book added successfully');
    } catch (error) {
        console.log(error);
        return res.status(500).send({ error: "Internal Server error" });
    }
}
module.exports.addReview= async (req, res, next) => {
    // documentation
    // this function is used to add a new review to the database
    // req.body should contain the following fields
    // review
    // the function will return 201 if the review is added successfully
    // the function will return 400 if the book does not exist
    // the function will return 400 if the request body is not valid
    // the function will return 500 if there is an internal server error
    // the function will return 400 if the author does not exist
    // the function will return 400 if the user does not exist
    // the function will return 400 if the user has already reviewed the book
    // the function will return 400 if the user has already read the book
    // the function will return 400 if the user has already rated the book
    // the function will return 400 if the user has already added the book to his/her reading list
    console.log("inside post review function")
    let { error } = validateReview(req.body);
    if (error) return res.status(400).send(error.details[0].message);
    console.log(req.body);
    let book = await Book.findById(req.params.id);
    if (!book){return res.status(400).send('Book does not exist');}
    let sentiment;
    const review = new Review({
        review:req.body.review,
        userId:req.user._id
    })
    const url = 'https://nextreadsrecommender.azurewebsites.net/sentiment'
    // const url = 'http://localhost:5000/sentiment'
    const body = {review:req.body.review}
    console.log(body);
    const response = await fetch(url,{method:'POST',body:JSON.stringify(body),headers: { 'Content-Type': 'application/json' }});
    sentiment = await response.json();//assuming data is json
    console.log(sentiment);
    review.sentiment=sentiment;
    book.reviews.push(review);
    try {
        await book.save();
        console.log(review);
        return res.status(201).send('Review added successfully');
    } catch (error) {
        console.log(error);
        return res.status(500).send({ error: "Internal Server error" });
    }
    
}
module.exports.getBooks= async (req, res, next) => {
    // documentation
    // this function is used to get all books from the database
    // the function will return 200 if the books are returned successfully
    // the function will return 404 if there are no books in the database
    // the function will return 500 if there is an internal server error
    booksPerPage = 15;
    if (!req.query.page) return res.status(400).send('Please specify page number');
    let page = parseInt(req.query.page);
    let books = await Book.find().populate('Author').skip((page-1)*booksPerPage).limit(booksPerPage);  
    if (books.length==0) return res.status(404).send('No books found');
    return res.status(200).send(books);
}

module.exports.addRating= async (req, res, next) => {
    // documentation
    // this function is used to add a new rating to the database
    // req.body should contain the following fields
    // rating
    // the function will return 201 if the rating is added successfully
    // the function will return 400 if the book does not exist
    // the function will return 400 if the request body is not valid
    // the function will return 500 if there is an internal server error
    // the function will return 400 if the author does not exist
    // the function will return 400 if the user does not exist
    // the function will return 400 if the user has already rated the book
    // the function will return 400 if the user has already read the book
    let { error } = validateRating(req.body);
    if (error) return res.status(400).send(error.details[0].message);
    console.log("here",req.params.id)
    console.log(req.body)
    let book = await Book.findById(req.params.id);
    if (!book){return res.status(400).send('Book does not exist');}
    let user = await User.findById(req.user._id);
    if (!user){return res.status(400).send('User does not exist, please sign out and try again');}
    let rating=book.avgRating*book.ratingCount;
    rating+=req.body.rating;
    book.ratingCount+=1;
    
    if(rating/book.ratingCount>5){
        book.avgRating=5;
    }
    else{
        book.avgRating=rating/book.ratingCount;
    }
    // if user has already rated the book, update the rating else add a new rating
    let read = user.read.find(r=>r.bookId==req.params.id);
    if(read){
        user.read = user.read.filter(r=>r.bookId!=req.params.id);
    }
    
    read= new Read({
        bookId:req.params.id,
        rating:req.body.rating
    })
    user.read.push(read);
    
    try {
        await book.save();
        await user.save();
        return res.status(201).send('Rating added successfully');
    } catch (error) {
        console.log(error);
        return res.status(500).send({ error: "Internal Server error" });
    }
}

module.exports.addRatings= async (req, res, next) => {
    // documentation
    // this function is used to add a new rating to the database
    // req.body should contain the following fields
    // ratings
    // the function will return 201 if the rating is added successfully
    // the function will return 400 if the book does not exist
    // the function will return 400 if the request body is not valid
    // the function will return 500 if there is an internal server error
    // the function will return 400 if the author does not exist
    // the function will return 400 if the user does not exist  
    // the function will return 400 if the user has already rated the book
    for(let rating of req.body.ratings){
        console.log(rating);
        let { error } = validateRating(rating);
        if (error) return res.status(400).send(error.details[0].message);
    }
    let user = await User.findById(req.user._id);
    if (!user){return res.status(400).send('User does not exist, please sign out and try again');}
    // find books from the list of ids
    let books = await Book.find({ _id: { $in: req.body.ratings.map(rating=>rating.bookId) } });
    if (!books){return res.status(400).send('Book does not exist');}
    // console.log(books);
    // convert ratings.bookId and ratings.rating to object key value pairs
    let ratings = req.body.ratings.reduce((acc, rating) => {
        acc[rating.bookId] = rating.rating;
        return acc;
    }, {});
    

    for (let book of books){
        // if rating is null set to 0
        if (!book.avgRating) book.avgRating = 0;
        // if rating_sum is null set to 0
        // if (!book.rating_sum) book.rating_sum = 0;
        // if rating_count is null set to 0
        if (!book.ratingCount) book.ratingCount = 0;
        let rating=book.avgRating*book.ratingCount;
        rating+=ratings[book._id];
        book.ratingCount+=1;
        book.avgRating=rating/book.ratingCount;
        const read= new Read({
            bookId:book._id,
            rating:ratings[book._id]
        })
        user.read.push(read);
        console.log(book)
        try {
            await book.save();
        } catch (error) {
            console.log(error);
            return res.status(500).send({ error: "Internal Server error" });
        }
    }

    try {
        await user.save();
        return res.status(201).send('Rating added successfully');
    } catch (error) {
        console.log(error);
        return res.status(500).send({ error: "Internal Server error" });
    }
}


module.exports.Recommender= async (req, res, next) => {
    // documentation
    // this function is used to recommeend books to the user
    // the function will take as parameter the user id
    // the function will return a list of books sorted by rating and sentiement score
    // the function will return 200 if the books are recommended successfully
    // the function will return 400 if the user does not exist
    // the function will return 500 if there is an internal server error


    let user = await User.findById(req.user._id).populate('read.bookId', 'bookId');
    if (!user){return res.status(400).send('User does not exist, please sign out and try again');}
    // change single quoted req.user._id to double quotes

    let ratings = user.read.reduce((acc, rating) => {
        var bookid= rating.bookId.bookId;
        acc[bookid] = rating.rating;
        return acc;
    }, {});

    request={
        user_id: req.user._id.toString(),
        books: ratings
    }

    const url = 'https://nextreadsrecommender.azurewebsites.net/RecommendUserBook'
    // const url = 'http://localhost:5000/RecommendUserBook'
    const body = request
    const response = await fetch(url,{method:'POST',body:JSON.stringify(body),headers: { 'Content-Type': 'application/json' }});
    let books = await response.json();//assuming data is json
    // console.log(books);
    // let recommendedBooks=[];
    // for (let author of authors){

    //     let authorBooks=await Book.find({ _id: { $in: author.books } });
    //     if (!authorBooks){return res.status(400).send('Book does not exist');}
    //     recommendedBooks.push(authorBooks);
    // }
    // get list of books from the dict of books
    // console.log(Object.keys(books))
    let recommendedBooks = await Book.find({ bookId: { $in: Object.keys(books) } }).select('bookId title author avgRating ratingCount imageUrl sentimentCount sentimentAvg');

    if (!recommendedBooks){return res.status(400).send('Books does not exist');}
    //  
    // for every book in recommendedBooks, add the rating from the dict of books
    let recommendedBooks2=[];
    for (let book of recommendedBooks){
        // console.log(book.ratingCount);
        let cRating = books[book.bookId]*3+(book.ratingCount/500000)+(book.sentimentCount/5000)+book.sentimentAvg*20;

        book={
            ...book._doc,
            CFrating:books[book.bookId],
            // combinedRating is a rating that combines sentiment score with Cf rating and average rating and rating count and sentiment count
            combinedRating:cRating
        }
        
        recommendedBooks2.push(book);
        // console.log(book);
        // break;
    }
    // sort recommendedBooks by rating
    recommendedBooks2.sort((a,b)=>b.combinedRating-a.combinedRating);
    // console.log(recommendedBooks);
    // get the top 20 books
    recommendedBooks2=recommendedBooks2.slice(0,20);
    return res.status(200).send(recommendedBooks2);


    // return res.status(200).send(user.read);
}

// module.exports.editEvent= async (req, res, next) => {
//     let { error } = validateScreeningRoom(_.pick(req.body,['screeningRoom']));
//     if (error) return res.status(400).send(error.details[0].message);
//     // let date1=new Date(req.body.date);
//     // const offset=date1.getTimezoneOffset();
//     // date1=new Date(date1.getTime()-(offset*60*1000));
//     const startTime=req.body.startTime;
//     const endTime=req.body.endTime;
//     const range = [startTime.hour, startTime.hour+1 ,endTime.hour];
//     let events = await Event.find({_id: { $ne: req.params.id } ,"screeningRoom":req.body.screeningRoom, 'date':req.body.date,'startTime.hour': range,'endTime.hour': range});
//     if (events.length>0) {
//         // if((event.startTime.hour<req.body.startTime.hour && event.endTime.hour>req.body.startTime.hour )
//         //     || (event.startTime.hour<req.body.endTime.hour && event.endTime.hour>req.body.endTime.hour))
//         return res.status(400).send('Event already exists at requested timeslot');
//     }
//     let seats;
//     if(req.body.screeningRoom=="1")
//     {
//         seats=20;
//     }
//     else
//     {
//         seats=30;
//     }
//     let event = await Event.findOneAndUpdate({"_id":req.params.id},
//     { 'startTime': req.body.startTime,
//     'endTime': req.body.endTime,
//     'date': req.body.date,
//     'screeningRoom': req.body.screeningRoom,
//     'seatsAmount':seats
//     });
    
//     try {
//         await event.save();
//         return res.status(201).send('Event edited successfully');
//     } catch (error) {
//         console.log(error);
//         return res.status(500).send({ error: "Internal Server error" });
//     }
// }

// module.exports.getEvents=async (req, res, next)=>{
//     let events=await Event.find({'movieId':req.params.movieId}).select('-__v');
//     // console.log(events);
//     // for(let i=0; i<events.length; i++)
//     // {
//     //     let dateold=events[i].date.toISOString().slice(0,10);
//     //     delete events[i].date;
//     //     events[i]["datee"]=dateold;
//     //     console.log(events[i]["datee"]);
//     // }
//     return res.status(201).send(events);
// }

// module.exports.getEvent=async (req, res, next)=>{
//     let events=await Event.find({_id:req.params.id}).populate('movieId','title imageUrl').select('-__v');
//     return res.status(201).send(events);
// }

// module.exports.getSeats= async (req, res, next) => {
//     const seats=await Event.findById(req.params.eventId).select('reservedSeats.seat');
//     console.log(seats);
//     return res.status(201).send(seats.reservedSeats);
// }