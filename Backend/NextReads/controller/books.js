const {validateBook,  Book,validateReview,Review}=require('../models/book')
const {Author,validateAuthor}=require('../models/author')
const _=require('lodash');
const spawn = require("child_process").spawn;


module.exports.addBook= async (req, res, next) => {
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
        Author: author._id
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
    let { error } = validateReview(req.body);
    if (error) return res.status(400).send(error.details[0].message);
    let book = await Book.findById(req.params.id);
    if (!book){return res.status(400).send('Book does not exist');}
    // running function getReviewSentiment() from classifier.py with req.body.review as argument and capturing the output
    // let sentiment = spawn('python3', ['-c', `from SentimentAnalysis.classifier import getReviewSentiment; print(getReviewSentiment('${req.body.review}'))`]);
    let sentiment;
    const review = new Review({
        review:req.body.review,
        rating:req.body.rating,
        userId:req.user._id
    })


    // run anaconda python script with arguments
    const pythonProcess = spawn('python3',["../../SentimentAnalysis/reviewClassifier.py", req.body.review]);
    // const pythonProcess = spawn('python3',["../../SentimentAnalysis/reviewClassifier.py", req.body.review]);
    // set sentiment to the output of the python script and save sentiment to the book
    pythonProcess.stdout.on('data', async (data) => {
        // Do something with the data returned from python script
        sentiment = data.toString();
    });
    // in close event we are sure that stream from child process is closed
    pythonProcess.on('close', async (code) => {
        console.log(`child process close all stdio with code ${code}`);
        // send data to browser
        // res.send(dataToSend)
        review.sentiment=sentiment;
        book.reviews.push(review);
        try {
            await book.save();
            return res.status(201).send('Review added successfully');
        } catch (error) {
            console.log(error);
            return res.status(500).send({ error: "Internal Server error" });
        }
        
    });
    



 
    
}
module.exports.getBooks= async (req, res, next) => {
    let books = await Book.find().populate('Author');
    if (books.length==0) return res.status(404).send('No books found');
    return res.status(200).send(books);
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