const mongoose = require('mongoose');
const app = require('./app');
const config = require('config');
// $env:JWTPRIVATEKEY="mySecureKey"   ---command to set environment variable 
console.log(process.env['JWTPRIVATEKEY']);
if (!process.env['JWTPRIVATEKEY']) {
    console.error('FATAL ERROR: JWTPRIVATEKEY is not defined.');
    process.exit(1);
  }


mongoose.connect('mongodb+srv://brutefoursteam:1234@nextreads.phkbn.mongodb.net//test')
    .then(() => console.log('connected to MongoDB'))
    .catch(err => console.error('could not connect to MongoDB', err));

const port = process.env.PORT || 80;
app.listen(port, () => console.log(`listening on port ${port}`));
//404 not found
// 400 bad request


