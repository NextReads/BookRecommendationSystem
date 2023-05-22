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
    // console.log("inside post review function")
    let { error } = validateReview(req.body);
    if (error) return res.status(400).send(error.details[0].message);
    // console.log(req.body);
    let book = await Book.findById(req.params.id);
    if (!book){return res.status(400).send('Book does not exist');}
    let sentiment;
    //if user already reviewed the book, remove the review and add the new one
    let review = book.reviews.find(r=>r.userId==req.user._id);
    if (review){
        book.reviews.pull(review);
    }
    review = new Review({
        review:req.body.review,
        userId:req.user._id
    })
    const url = 'https://nextreadsrecommender.azurewebsites.net/sentiment'
    // const url = 'http://localhost:5000/sentiment'
    const body = {review:req.body.review}
    const response = await fetch(url,{method:'POST',body:JSON.stringify(body),headers: { 'Content-Type': 'application/json' }});
    sentiment = await response.json();//assuming data is json
    review.sentiment=sentiment;
    book.reviews.unshift(review);
    try {
        await book.save();
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
    //find books and sort by ratingCount
    let books = await Book.find().skip((page-1)*booksPerPage).limit(booksPerPage).sort({ratingCount:-1}).select('bookId title authors avgRating imageUrl description ratingCount'); 
    //get book authors
    // for (let i=0;i<books.length;i++){
    //     books[i]._doc.populatedAuthors = [];
    //     for (let j=0;j<books[i].authors.length;j++){
    //         let author = await Author.find({"author_id":books[i].authors[j]})
    //         let x = {
    //             "author_id":author[0].author_id,
    //             "name":author[0].full_name,
    //         }
    //         books[i]._doc.populatedAuthors.push(x);
    //     }
    // }  
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
    user.read.unshift(read);
    
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
        let { error } = validateRating(rating);
        if (error) return res.status(400).send(error.details[0].message);
    }
    let user = await User.findById(req.user._id);
    if (!user){return res.status(400).send('User does not exist, please sign out and try again');}
    // find books from the list of ids
    let books = await Book.find({ _id: { $in: req.body.ratings.map(rating=>rating.bookId) } });
    if (!books){return res.status(400).send('Book does not exist');}
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
        // console.log(book)
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
    // get list of books from the dict of books
    let recommendedBooks = await Book.find({ bookId: { $in: Object.keys(books) } }).select('bookId title authors avgRating ratingCount imageUrl sentimentCount sentimentAvg');

    if (!recommendedBooks){return res.status(400).send('Books does not exist');}
    //  
    // for every book in recommendedBooks, add the rating from the dict of books
    let sentimentHeaderCheck = response.headers.get('sentiment');
    console.log(sentimentHeaderCheck);
    let recommendedBooks2=[];
    for (let book of recommendedBooks){
        cfRatingRet = books[book.bookId];
        // if sentimentHeaderCheck is true, add sentiment score to book
        if (bool(sentimentHeaderCheck)){
            cfRatingRet = books[book.bookId]
        }
        else{
            cfRatingRet = 0;
        }
        let cRating = cfRatingRet*3+(book.ratingCount/500000)+(book.sentimentCount/5000)+book.sentimentAvg*20;

        book={
            ...book._doc,
            CFrating:cfRatingRet,
            // combinedRating is a rating that combines sentiment score with Cf rating and average rating and rating count and sentiment count
            combinedRating:cRating
        }
        
        recommendedBooks2.push(book);
        // break;
    }
    // sort recommendedBooks by rating
    recommendedBooks2.sort((a,b)=>b.combinedRating-a.combinedRating);
    // get the top 20 books
    recommendedBooks2=recommendedBooks2.slice(0,20);
    let authors=recommendedBooks2.map(book => book.authors);
    // unpack list of authors and save them in authors array
    authors = authors.reduce((acc, val) => acc.concat(val), []);
    authors_full_name = await Author.find({ author_id: { $in: authors } }).select('full_name author_id');
    
    // map each authors_full_name to each entry in list of book authors
    recommendedBooks2.forEach(book => {
        book.authors = book.authors.map(author => authors_full_name.find(author_full_name => author_full_name.author_id == author).full_name);
    });



    return res.status(200).send(recommendedBooks2);


    // return res.status(200).send(user.read);
}

module.exports.getBook= async (req, res,next) =>{
    // this function is used to get a book by id
    // the function will take as parameter the book id
    // the function will return 200 if the book is found
    // the function will return 404 if the book does not exist
    // the function will return 500 if there is an internal server error
    let book = await Book.findById(req.params.id).select('bookId title authors avgRating imageUrl description ratingCount genres');
    if (!book){return res.status(404).send('Book does not exist');}
    // get book authors by author id
    let authors = await Author.find({ author_id: { $in: book.authors } }).select('full_name');
    if (!authors){return res.status(404).send('Author does not exist');}
    book={
        ...book._doc,
        authors:authors
    }

    return res.status(200).send(book);
}
module.exports.searchBooks= async (req, res,next) =>{
    // this function is used to search for books by title, author, genre, or description by page 
    // the function will take as parameter the search query
    // the function will return 200 if the books are found
    // the function will return 404 if the books do not exist
    // the function will return 500 if there is an internal server error
    // the function will return 400 if the search query is empty
    // the function will return 400 if the page number is not a number
    // the function will return 400 if the page number is less than 1
    // the function will return 400 if the page number is greater than the number of pages
    // the function will return 400 if the page number is not an integer 

    // the request should be as follows
    // http://localhost:3000/api/books/search?search=the&pageNumber=1
    // the route handler will be as follows
    // router.get('/search',auth,booksController.searchBooks);
    // console.log(req.query.search);
    // console.log(req);
    pageNumber = req.query.pageNumber;
    // console.log(req.query.search);
    // console.log(pageNumber);
    if (!pageNumber){return res.status(400).send('Page number is required');}
    if (isNaN(pageNumber)){return res.status(400).send('Page number must be a number');}
    if (pageNumber<1){return res.status(400).send('Page number must be greater than 0');}
    let booksPerPage=20;
    const books = await Book.find({ title: { $regex: req.query.search, $options: "i" } })
        // .or([{ title: { $regex: req.query.search, $options: "i" } }, { description: { $regex: req.query.search, $options: "i" } }])
        // .populate('Avatar', 'photoUrl -_id')
        .select('bookId title authors avgRating ratingCount imageUrl sentimentCount sentimentAvg genres')
        // .sort({ avgRating: -1 })
        .skip((pageNumber-1)*booksPerPage).limit(booksPerPage);
    if (!books){return res.status(404).send('Books do not exist');}
    // get list of authors from books.aurhors
    let authors=books.map(book => book.authors);
    // console.log(authors);
    // unpack list of authors and save them in authors array
    authors = authors.reduce((acc, val) => acc.concat(val), []);
    // console.log(authors);
    authors_full_name = await Author.find({ author_id: { $in: authors } }).select('full_name author_id');
    // console.log(authors_full_name);
    // map each authors_full_name to each entry in list of book authors
    books.forEach(book => {
        book.authors = book.authors.map(author => authors_full_name.find(author_full_name => author_full_name.author_id == author).full_name);
    });

    // sort books where title includes search query then description includes search query
    // books=books.sort((a,b)=>(a.title.includes(req.query.search)?0:1)-(b.title.includes(req.query.search)?0:1)||(a.description.includes(req.query.search)?0:1)-(b.description.includes(req.query.search)?0:1));
    let numberOfBooks = await Book.countDocuments({ title: { $regex: req.query.search, $options: "i" } });
    let numberOfPages=Math.ceil(numberOfBooks/booksPerPage);
    if (pageNumber>numberOfPages){return res.status(400).send('Page number must be less than or equal to '+numberOfPages);}
    return res.status(200).send({books:books,numberOfPages:numberOfPages});
    // return res.status(200).send(books);
    
}


module.exports.getByGenre= async (req, res,next) =>{
    // this function is used to search for books by genre
    // the function will take as parameter the search query
    // the function will return 200 if the books are found
    // the function will return 404 if the books do not exist
    // the function will return 500 if there is an internal server error
    // the function will return 400 if the search query is empty
    // the function will return 400 if the page number is not a number
    // the function will return 400 if the page number is less than 1
    // the function will return 400 if the page number is greater than the number of pages
    // the function will return 400 if the page number is not an integer 

    // the request should be as follows
    // http://localhost:3000/api/books/search?search=the&pageNumber=1
    // the route handler will be as follows
    // router.get('/search',auth,booksController.searchBooks);
    // console.log(req.query.search);
    // console.log(req);
    pageNumber = req.query.pageNumber;
    console.log(req.query.genre);
    console.log(pageNumber);
    if (!pageNumber){return res.status(400).send('Page number is required');}
    if (isNaN(pageNumber)){return res.status(400).send('Page number must be a number');}

    if (pageNumber<1){return res.status(400).send('Page number must be greater than 0');}
    let booksPerPage=16;
    const books = await Book.find({ genres: { $regex: req.query.genre, $options: "i" } })
        // .or([{ title: { $regex: req.query.search, $options: "i" } }, { description: { $regex: req.query.search, $options: "i" } }])
        .select('bookId title authors avgRating ratingCount imageUrl sentimentCount sentimentAvg genres')
        .sort({ ratingCount: -1 })
        .skip((pageNumber-1)*booksPerPage).limit(booksPerPage);
    if (!books){return res.status(404).send('Books do not exist');}
    // get list of authors from books.aurhors
    let authors=books.map(book => book.authors);
    // console.log(authors);
    // unpack list of authors and save them in authors array
    authors = authors.reduce((acc, val) => acc.concat(val), []);
    // console.log(authors);
    authors_full_name = await Author.find({ author_id: { $in: authors } }).select('full_name author_id');
    // console.log(authors_full_name);
    // map each authors_full_name to each entry in list of book authors
    books.forEach(book => {
        book.authors = book.authors.map(author => authors_full_name.find(author_full_name => author_full_name.author_id == author).full_name);
    });

    let numberOfBooks = await Book.countDocuments({ genres: { $regex: req.query.genre, $options: "i" } });
    let numberOfPages=Math.ceil(numberOfBooks/booksPerPage);
    if (pageNumber>numberOfPages){return res.status(400).send('Page number must be less than or equal to '+numberOfPages);}
    return res.status(200).send({books:books,numberOfPages:numberOfPages});
    // return res.status(200).send(books);
    
}
// module.exports.getByGenresArray= async (req, res,next) =>{
//     pageNumber = req.query.pageNumber;
//     console.log(req.query.genres);
//     console.log(pageNumber);
//     if (!pageNumber){return res.status(400).send('Page number is required');}
//     if (isNaN(pageNumber)){return res.status(400).send('Page number must be a number');}
//     if (pageNumber<1){return res.status(400).send('Page number must be greater than 0');}
//     let booksPerPage=20;
//     const books = await Book.find({ genres: { $in: req.query.genres } })
//         // .or([{ title: { $regex: req.query.search, $options: "i" } }, { description: { $regex: req.query.search, $options: "i" } }])
