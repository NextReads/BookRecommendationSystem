const {Author,validateAuthor}=require('../models/author')
const _=require('lodash');

module.exports.addAuthor= async (req, res, next) => {

    let { error } = validateAuthor(_.pick(req.body,['firstName','middleName','lastName']));
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