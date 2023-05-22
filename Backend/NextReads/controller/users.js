const { User, validateLogin, validateSignup } = require('../models/user')
const { Book } = require('../models/book')
const bcrypt = require('bcrypt');

module.exports.register = async (req, res, next) => {
    let { error } = validateSignup(req.body);
    if (error) return res.status(400).send(error.details[0].message);
    let user = await User.findOne({ $or: [{ email: req.body.email }, { username: req.body.username }] });
    if (user) return res.status(400).send('User already registered');
    // if(user) return res.status(400).send(user);
    user = new User({
        firstName: req.body.firstName,
        lastName: req.body.lastName,
        email: req.body.email,
        username: req.body.username,
        password: req.body.password
    });
    const salt = await bcrypt.genSalt(10);
    user.password = await bcrypt.hash(user.password, salt);
    if(req.body.role ==="Manager")
    {
        user.requestingAuthority=true;
    }
    try {
        const token = user.generateAuthToken();
        await user.save();
        return res.status(201).header('x-auth-token', token).send('success1');
    } catch (error) {
        console.log(error);
        res.status(500).send({ error: "Internal Server error" });
    }
}

module.exports.logIn = async (req, res, next) => {
    let { error } = validateLogin(req.body);
    if (error) return res.status(400).send(error.details[0].message);

    let user = await User.findOne({ username: req.body.username });
    if (!user) return res.status(400).send('Invalid email or password.');
    const validPassword = await bcrypt.compare(req.body.password, user.password);
    if (!validPassword) return res.status(400).send('Invalid email or password.');

    const token = user.generateAuthToken();
    return res.status(201).header('x-auth-token', token).send('success');
    // return res.status(200).send(token);
}

module.exports.getUser= async (req, res, next) => {
    const user =await User.findOne({ _id: req.user._id }).select('-password -__v');
    res.send(user);
}

// module.exports.addtoRead = async (req, res, next) => {
//     // get user and add book to read list
//     const user = await User.findOne({ _id: req.user._id });
//     const book=await Book.findById( req.params.bookId);
//     if(!book) return res.status(404).send('The book with the given ID was not found.');
    
//     try{
//         user.read.push(book);
//         await user.save();
//         return res.status(201).send("book added successfully");
//     } catch (error) {
//         console.log(error);
//         res.status(500).send({ error: "Internal Server error" });
//     }
// }

module.exports.authorize= async (req, res, next) => {
    
    try {
        let users= await User.updateMany({ _id: req.body.id, requestingAuthority:true},
            { $set:{'requestingAuthority':'false','isManager':'true'}});
    
        if(!users) return res.status(500).send({ error: "Internal Server error" });
        if(users.length ==0) return res.status(404).send('No users found.');
        return res.status(201).send(users);;
    } catch (error) {
        console.log(error);
        return res.status(500).send({ error: "Internal Server error" });
    }
    
}

module.exports.getRequestingUsers= async (req, res, next) => {
    let users=await User.find({requestingAuthority:true}).select('-password -__v');
    if(!users) return res.status(500).send({ error: "Internal Server error" });
    if(users.length ==0) return res.status(404).send('No users found.');
    res.send(users);
}
module.exports.getUsers= async (req, res, next) => {
    let users=await User.find().select('-password -__v');
    res.send(users);
}

module.exports.deleteUser= async (req, res, next) => {
    try{
        const book =await Book.updateMany({'reviews.userId':req.params.id},{"$pull":{"reviews":{userId:req.params.id}}});
        const user = await User.findOneAndDelete({_id:req.params.id});
        if(!user) return res.status(404).send({ error: "user not found" });
        return res.status(201).send('user successfully deleted');
    } catch (error) {
        console.log(error);
        return res.status(500).send({ error: "Internal Server error" });
    }
}

module.exports.getReadBooks= async (req, res, next) => {
    const books = await User.findOne({ _id: req.user._id }).select('read').populate('read').populate('read.bookId');
    
    //check if user rated the book
    let readBooksCount = books.read.length;
    readbooks = books.read;
    

    for (let i = 0; i < readBooksCount; i++) {
        let reviewsCount = readbooks[i].bookId.reviews.length;
        for (let j = 0; j < reviewsCount; j++) {
            if (readbooks[i].bookId.reviews[j].userId == req.user._id) {
                let review =readbooks[i].bookId.reviews[j].review
                readbooks[i]._doc.userReview = review;
                break;
            }
        }
    }
    return res.status(201).send(readbooks);
}

module.exports.getWantToRead= async (req, res, next) => {
    const books = await User.findOne({ _id: req.user._id }).select('wantToRead').populate('wantToRead').populate('read.bookId');//.select('-__v -read.__v -read.reviews -read.reviews.userId -read.reviews.__v');
    return res.status(201).send(books.wantToRead);
}

module.exports.getCurrentlyReading= async (req, res, next) => {
    const books = await User.findOne({ _id: req.user._id }).select('currentlyReading').populate('currentlyReading').populate('read.bookId');//.select('-__v -read.__v -read.reviews -read.reviews.userId -read.reviews.__v');
    return res.status(201).send(books);
}
//get number of rated books by user
module.exports.getRatedBooks= async (req, res, next) => {
    const books = await User.findOne({ _id: req.user._id }).select('read').populate('read').populate('read.bookId');
    let count=0;
    books.read.forEach(book => {
        if(book.rating!=0)
        {
            count++;
        }
    });
    return res.status(200).send({count:count});
}
module.exports.addToWantToRead= async (req, res, next) => {
    const book=await Book.findById( req.params.bookId);
    if(!book) return res.status(404).send('The book with the given ID was not found.');
    
    try{
        const user = await User.findOne({ _id: req.user._id });
        if(user.wantToRead.includes(book._id)) return res.status(400).send('Book already in want to read list');
        user.wantToRead.push(book);
        await user.save();
        return res.status(201).send("book added successfully");
    } catch (error) {
        console.log(error);
        res.status(500).send({ error: "Internal Server error" });
    }
}
module.exports.toReadNext= async (req, res, next) => {
    const book=await Book.findById( req.params.bookId);
    if(!book) return res.status(404).send('The book with the given ID was not found.');
    
    try{
        const user = await User.findOne({ _id: req.user._id });
        user.toReadNext=book;
        await user.save();
        return res.status(201).send("book added successfully");
    } catch (error) {
        console.log(error);
        res.status(500).send({ error: "Internal Server error" });
    }
}
module.exports.getToReadNext= async (req, res, next) => {
    const book=await User.findOne({ _id: req.user._id }).select('toReadNext').populate('toReadNext');
    if (!book) return res.status(404).send('book not found');
    return res.status(200).send(book.toReadNext);
}
module.exports.searchInRead= async (req, res, next) => {
    //search for a regex in read books titles
        if(!req.query.search) return res.status(400).send('search query not found')
        const books = await User.findOne({ _id: req.user._id }).select('read').populate('read').populate('read.bookId');
        let readBooksCount = books.read.length;
        readbooks = books.read;
        let result=[];
        for (let i = 0; i < readBooksCount; i++) {
            if(readbooks[i].bookId.title.toLowerCase().includes(req.query.search.toLowerCase()))
            {
                result.push(readbooks[i]);
            }
        }
        return res.status(200).send(result);

    
}
module.exports.searchInTbr= async (req, res, next) => {
    //search for a regex in read books titles
        if(!req.query.search) return res.status(400).send('search query not found')
        const books = await User.findOne({ _id: req.user._id }).select('wantToRead').populate('wantToRead').populate('read.bookId');
        let readBooksCount = books.wantToRead.length;
        readbooks = books.wantToRead;
        let result=[];
        for (let i = 0; i < readBooksCount; i++) {
            if(readbooks[i].title.toLowerCase().includes(req.query.search.toLowerCase()))
            {
                result.push(readbooks[i]);
            }
        }
        return res.status(200).send(result);

    
}
