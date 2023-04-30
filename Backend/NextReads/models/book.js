const Joi = require('joi');
const mongoose = require('mongoose');

const reviewSchema = new mongoose.Schema({
    // define review rating
    rating: {
        type: Number,
        required: true,
        trim: true,
        min: 0,
        max: 5
    },
    // define review sentiment
    sentiment: {
        type: Number,
        required: true,
        trim: true,
        min: 0,
        max: 1
    },
    // define review
    review: {
        type: String,
        required: false,
        trim: true,
        minlength: 1,
        maxlength: 1024
    },
    userId: {
        type: mongoose.Schema.Types.ObjectId,
        required: true,
        ref: 'User'
    }
});

const Review = mongoose.model('Review', reviewSchema);


const Book = mongoose.model('Book', new mongoose.Schema({
    title: {
        type: String,
        required: true,
        trim: true,
        minlength: 5,
        maxlength: 255
    },
    Author:{
        type: mongoose.Schema.Types.ObjectId,
        required: true,
        ref: 'Author'        
    },
    imageUrl:{
        type: String,
        minlength: 5,
        maxlength: 1024,
        required: true
    },
    avgRating:{
            type: Number,
            required: true,
            default: 0,
            trim: true,
            min: 0,
            max: 5
    },
    ratingCount:{
        type: Number,
            required: true,
            trim: true,
            default: 0,
            min: 0,
    },
    isbn:{
        type: String,
        required: false,
        trim: true,
        minlength: 10,
        maxlength: 13
    },
    genre:{
        type: String,
        required: false,
        trim: true,
        minlength: 1,
        maxlength: 255
    },
    bookId:{
        type: String,
        required: true,
        trim: true,
        minlength: 1,
        maxlength: 255
    },
    year:{
        type: Number,
        required: false,
        trim: true,
        min: 0
        },

    reviews:[reviewSchema]
}));


function validateBook(book) {
    const schema = Joi.object({
        title: Joi.string().min(5).max(255).required(),
        imageUrl: Joi.string().min(5).max(1024).required(),
        isbn: Joi.string().min(10).max(13),
        genre: Joi.string().min(1).max(255),
    });

    return schema.validate(book);
}
function validateReview (body) {
    const schema = Joi.object({
        review: Joi.string().min(1).max(1024).required()
    });

    return schema.validate(body);
};

exports.Review = Review;
exports.Book = Book; 
exports.validateBook = validateBook;
exports.validateReview = validateReview
