const fs = require('fs');

module.exports = {
    'mongoUrl': fs.readFileSync(__dirname + '/config/mongo-url', 'utf-8')
};