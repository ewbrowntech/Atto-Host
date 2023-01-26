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
router.post('/signup', (request, response, next) => {
  User.register(new User({username: request.body.username}), request.body.password, (err, user) => {
    if (err) {
      response.statusCode = 500;
      response.setHeader('Content-Type', 'application/json');
      response.json({err: err});
    } else {
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
    const token = authenticate.getToken({_id: request.user._id});
    response.statusCode = 200;
    response.setHeader('Content-Type', 'application/json');
    response.json({success: true, token: token, status: 'Login successful!'});
  }
});

module.exports = router;
