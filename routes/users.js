const express = require('express');
const bodyParser = require('body-parser');
const User = require('../models/user');

const router = express.Router();
router.use(bodyParser.json());

/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('respond with a resource');
});

router.post('/signup', (request, response, next) => {
  User.register(new User({username: request.body.username}), request.body.password, (err, user) => {
    if (err) {
      response.statusCode = 500;
      response.setHeader('Content-Type', 'application/json');
      response.json({err: err});
    } else {
      user.save((err, user) => {
        if (err) {
          response.statusCode = 500;
          response.setHeader('Content-Type', 'application/json');
          response.json({err: err});
          return
        } else {
          response.statusCode = 200;
          response.setHeader('Content-Type', 'application/json');
          response.json({success: true, status: 'Registration successful!'});
        }
      });
    }
  });
});

module.exports = router;
