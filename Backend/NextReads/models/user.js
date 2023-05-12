const Joi = require('joi');
const mongoose = require('mongoose');
Joi.objectId= require("joi-objectid")(Joi);
const jwt = require('jsonwebtoken');
const config = require('config');

const readSchema = new mongoose.Schema({
    bookId: {
        type: mongoose.Schema.Types.ObjectId,
        required: true,
        ref: 'Book'
    },
    rating: {
        type: Number,
        required: true,
        min: 1,
        max: 5
}});

const userSchema = new mongoose.Schema({
    username: {
        type: String,
        required: true,
        trim: true,
        minlength: 5,
        maxlength: 50,
        unique: true,
        dropDups: true,
    },
    password: {
        type: String,
        required: true,
        trim: true,
        minlength: 5,
        maxlength: 1024
    },
    firstName: {
        type: String,
        required: true,
        trim: true,
        minlength: 1,
        maxlength: 255
    },
    lastName: {
        type: String,
        required: true,
        trim: true,
        minlength: 1,
        maxlength: 255
    },
    email: {
        type: String,
        required: true,
        trim: true,
        minlength: 5,
        unique: true,
        dropDups: true,
    },
    requestingAuthority:{
        type:Boolean,
        default:false,
        required: true
    },
    isManager:{
        type:Boolean,
        default:false,
        required: true
    },
    isAdmin:{
        type:Boolean,
        default:false,
        required: true
    },
    Author: new mongoose.Schema({
        isAuthor: {
            type:Boolean,
            default:false,
            required: true},
        authorId: {
            type: mongoose.Schema.Types.ObjectId,
            ref: 'Author'
        }
    }),
    read: [readSchema],
    wantToRead:[{
        type: mongoose.Schema.Types.ObjectId,
        required: true,
        ref: 'Book'
    }],
    currentlyReading:{
        type: mongoose.Schema.Types.ObjectId,
        //required: true,
        ref: 'Book'
    },
    imageUrl: {
        type: String,
        // required: true,
        trim: true,
        minlength: 1,
        maxlength: 1024
    },
    bio: {
        type: String,
        // required: true,
        trim: true,
        minlength: 1,
        maxlength: 1024
    },
    toReadNext:{
        type: mongoose.Schema.Types.ObjectId,
        //required: true,
        ref: 'Book'
    }
});
userSchema.methods.generateAuthToken = function() { 
    const token = jwt.sign({ _id: this._id, isManager: this.isManager,isAdmin:this.isAdmin }, process.env['JWTPRIVATEKEY']);
    return token;
  }

const User = mongoose.model('User', userSchema);
const Read = mongoose.model('Read', readSchema);
// const Movie = mongoose.model('Movie', movieSchema);



function validateLogin(body) {
    const schema = Joi.object({
        username: Joi.string().min(5).max(50).required(),
        password: Joi.string().min(5).max(50).required(),
    });

    return schema.validate(body);

};

function validateSignup (body) {
    const schema = Joi.object({
        firstName: Joi.string().min(1).max(50).required(),
        lastName: Joi.string().min(1).max(50).required(),
        username: Joi.string().min(5).max(50).required(),
        email: Joi.string().email().required(),
        password: Joi.string().min(8).max(50).required(),
        role:Joi.string().min(5).max(10).required()
    });

    return schema.validate(body);
};

function validateRating(body) {
    const schema = Joi.object({
        bookId: Joi.objectId().required(),
        rating: Joi.number().min(1).max(5).required()
    });

    return schema.validate(body);
};



exports.User = User;
exports.Read = Read;
exports.validateLogin = validateLogin;
exports.validateSignup=validateSignup;
exports.validateRating=validateRating;