const jwt = require('jsonwebtoken');
const config = require('config');


module.exports = (req, res, next) => {
    const token = req.header('x-auth-token');
    if (!token) res.status(401).send('Access Denied. No token Provided');

    try {
        const decoded = jwt.verify(token, process.env['JWTPRIVATEKEY']);
        req.user = decoded;
        next();
    }
    catch (ex) {
        res.status(400).send('Invalid token.');
    }

}
