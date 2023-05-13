const {Author,validateAuthor}=require('../models/author')
const _=require('lodash');

module.exports.addAuthor= async (req, res, next) => {
    // documentation
    // this function is used to add a new author to the database
    // req.body should contain the following fields
    // fullName
    // the function will return 201 if the author is added successfully
    // the function will return 400 if the author already exists
    // the function will return 400 if the request body is not valid
    // the function will return 500 if there is an internal server error
    

    let { error } = validateAuthor(_.pick(req.body,['fullName']));
    if (error) return res.status(400).send(error.details[0].message);

    let author1 = await Author.findOne({$and: [{ firstName: req.body.firstName }, {middleName: req.body.middleName},{ lastName: req.body.lastName }]}) 
    if(author1){
        return res.status(400).send('an Author already exists by the same Name');
    }
  
    const author = new Author({
        firstName:req.body.firstName,
        middleName:req.body.middleName,
        lastName:req.body.lastName
    })
    try {
        await author.save();
        return res.status(201).send('Author added successfully');
    } catch (error) {
        console.log(error);
        return res.status(500).send({ error: "Internal Server error" });
    }

    }