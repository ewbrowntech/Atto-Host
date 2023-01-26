// Modules
const createError = require('http-errors');
const express = require('express');
const path = require('path');
const logger = require('morgan');
const mongoose = require('mongoose');
const passport = require('passport');
// Configuration
const config = require('./config');
// Routers
const indexRouter = require('./routes/index');
const userRouter = require('./routes/users');
const uploadRouter = require('./routes/upload');

// Connect to MongoDB Server
const mongoURL = config.mongoUrl;
mongoose.set("strictQuery", false);
const connect = mongoose.connect(mongoURL);
connect.then((db) => {
  console.log("Connected correctly to the MongoDB server!");
}, (err) => {console.log(err)});

let app = express();

app.use("/bootstrap", express.static(path.join(__dirname, "node_modules/bootstrap")));
app.use("/bootstrap-social", express.static(path.join(__dirname, "node_modules/bootstrap-social")));
app.use("/popper.js", express.static(path.join(__dirname, "node_modules/popper.js")));
app.use("/jquery", express.static(path.join(__dirname, "node_modules/jquery")));



// Set up view engine
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({extended: false}));
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/users', userRouter);
app.use('/upload', uploadRouter); // For handling uploads to the cloud storage

// If request was not forwarded via existing routes,
// then the requested resource does not exist (Error 404)
app.use(function(request, response, next) {
  next(createError(404));
});

// Error handler
app.use(function(err, request, response, next) {
  // set locals, only providing error in development
  response.locals.message = err.message;
  response.locals.error = request.app.get('env') === 'development' ? err : {};

  // render the error page
  response.status(err.status || 500);
  response.render('error', {title:'your_page_title'});
});

module.exports = app;