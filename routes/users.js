const express = require('express');
const bodyParser = require('body-parser');
const User = require('../models/user');
const passport = require('passport');
const authenticate = require('../authenticate');

const router = express.Router();
router.use(bodyParser.json());

/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('respond with a resource');
});

// Enable account signup
router.post('/signup', authenticate.verifyToken, authenticate.verifyAdmin, (request, response, next) => {
  User.register(new User({username: request.body.username, automated: request.body.automated}), request.body.password, (err, user) => {
    if (err) {
      response.statusCode = 500;
      response.setHeader('Content-Type', 'application/json');
      response.json({err: err});
    } else {
      if (user.automated == true) {
        User.findByIdAndUpdate()
      }
      user.save((err, user) => {
        passport.authenticate('local')(request, response, () => {
          if (err) {
            response.statusCode = 500;
            response.setHeader('Content-Type', 'application/json');
            response.json({err: err});
          } else {
            response.statusCode = 200;
            response.setHeader('Content-Type', 'application/json');
            response.json({success: true, status: 'Registration successful!'});
          }
        });
      });
    }
  });
});

// Enable account login, generating JWT token for further requests
router.post('/login', passport.authenticate('local'), (request, response) => {
  if (request.user) {
    const token = authenticate.getTemporaryToken({_id: request.user._id});
    response.statusCode = 200;
    response.setHeader('Content-Type', 'application/json');
    response.json({success: true, token: token, status: 'Login successful!'});
  }
});

// Enable account login, generating JWT token for further requests
router.post('/generate-api-key', authenticate.verifyToken, authenticate.verifyAdmin, passport.authenticate('local'), (request, response) => {
  if (request.user) {
    if (request.user.automated == true) {
      console.log(request.user._id);
      const token = authenticate.getPerpetualToken({_id: request.user._id});
      User.findOneAndUpdate({_id: request.user._id}, { $set: { api_key: token }}).then((user) => {});
      response.statusCode = 200;
      response.setHeader('Content-Type', 'application/json');
      response.json({success: true, token: token});
    } else {
      let err = new Error('You may not generate perpetual keys for non-automated accounts!');
      err.status = 403;
      return next(err);
    }
  }
});

module.exports = router;
