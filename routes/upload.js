const express = require('express');
const bodyParser = require('body-parser');
const multer = require('multer');

const storage = multer.diskStorage({
    destination: (request, response, callback) => {
        callback(null, 'public/storage');
    },
    filename: (request, file, callback) => {
        callback(null, file.originalname);
    }
});

// Do not allow the upload of executable files
const staticFileFilter = (request, file, callback) => {
    if (!file.originalname.match(/\.(jpg|jpeg|png|gif)$/)) {
        return callback(new Error('You may only upload media'), null);
    }
    callback(null, true);
};

const upload = multer({storage: storage, fileFilter: staticFileFilter});

const uploadRouter = express.Router();
uploadRouter.use(bodyParser.json());

uploadRouter.route('/')
    .get((request, response, next) => {
        response.statusCode = 403;
        response.end('GET operation not supported on /upload');
    })
    .post(upload.single('filename'), (request, response, next) => {
        response.statusCode = 200;
        response.setHeader('Content-Type', 'application/json');
        response.json(request.file);
    });

module.exports = uploadRouter;
