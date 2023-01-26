const fs = require('fs');

module.exports = {
    'secretKey': fs.readFileSync(__dirname + '/config/auth-secret-key', 'utf-8'),
    'mongoUrl': fs.readFileSync(__dirname + '/config/mongo-url', 'utf-8')
};