const Joi = require('joi');
const mongoose = require('mongoose');

const authorSchema = new mongoose.Schema({
    firstName: {
        type: String,
        required: true,
        trim: true,
        minlength: 1,
        maxlength: 50
    },
    middleName: {
        type: String,
        required: false,
        trim: true,
        minlength: 1,
        maxlength: 50
    },
    lastName: {
        type: String,
        required: false,
        trim: true,
        minlength: 1,
        maxlength: 50
    },
    fullName: {
        type: String,
        required: true,
        trim: true,
        minlength: 1,
        maxlength: 150
    },
    authorId:{
        type: String,
        required: true,
        trim: true,
        minlength: 1,
        maxlength: 150
    },
    books: [{
        type: mongoose.Schema.Types.ObjectId,
        required: true,
        ref: 'Book'
    }],
    userId:{
        type: mongoose.Schema.Types.ObjectId,
        required: false,
        ref: 'User'
    }
});

function validateAuthor (body) {
    const schema = Joi.object({
        firstName: Joi.string().min(1).max(50).required(),
        middleName: Joi.string().min(1).max(50),
        lastName: Joi.string().min(1).max(50).required()
    });

    return schema.validate(body);
};


const Author = mongoose.model('Author', authorSchema);

exports.Author = Author;
exports.validateAuthor = validateAuthor;