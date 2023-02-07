const mongoose = require('mongoose');
const Schema = mongoose.Schema;
const passportLocalMongoose = require('passport-local-mongoose');

let User = new Schema({
    admin: {
        type: Boolean,
        default: false
    },
    automated: {
        type: Boolean,
        default: false
    },
    api_key: {
        type: String,
        required: false
    }
});

User.plugin(passportLocalMongoose);
module.exports = mongoose.model('User', User);