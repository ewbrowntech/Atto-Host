const passport = require('passport');
const LocalStrategy = require('passport-local').Strategy;
const User = require('./models/user');
const JwtStrategy = require('passport-jwt').Strategy;
const ExtractJwt = require('passport-jwt').ExtractJwt;
const jwt = require('jsonwebtoken');

const config = require('./config');
const {response} = require("express");

exports.local = passport.use(new LocalStrategy(User.authenticate()));
passport.serializeUser(User.serializeUser());
passport.deserializeUser(User.deserializeUser());

// Generate a new JSON Web Token upon login for use in further authenticated requests
exports.getTemporaryToken = function(user) {
    return jwt.sign(user, config.secretKey, {expiresIn: 3600});
}

// Generate a new JSON Web Token upon login for use in further authenticated requests
exports.getPerpetualToken = function(user) {
    return jwt.sign(user, config.secretKey);
}

// Extract JSON Web Token from Authorization header of incoming requests
let opts = {};
opts.jwtFromRequest = ExtractJwt.fromAuthHeaderAsBearerToken();
opts.secretOrKey = config.secretKey;
exports.jwtPassport = passport.use(new JwtStrategy(opts, (jwt_payload, done) => {
    console.log("JWT Payload: ", jwt_payload);
    User.findOne({_id: jwt_payload._id}, (err, user) => {
        if (err) {
            return done(err, false);
        }
        else if (user) {
            return done(null, user);
        }
        else {  // If no error and no user returned, then user does not exist
            return done(null, false);
        }
    });
}));

// Verify that an incoming request is from a user that is currently logged in
exports.verifyToken = passport.authenticate('jwt', {session: false});

exports.verifyAdmin = (request, response, next) => {
    console.log("Username: " + request.user.username + " | Admin: " + request.user.admin);
    if (request.user.admin !== false) {
        next();
    } else {
        let err = new Error('You are not authorized to perform this operation!');
        err.status = 403;
        return next(err);
    }
}