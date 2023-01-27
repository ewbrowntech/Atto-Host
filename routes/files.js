const express = require('express');
const bodyParser = require('body-parser');
const authenticate = require('../authenticate');
const multer = require('multer');

// Schema for file info document
const Files = require('../models/file');

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

const fileRouter = express.Router();
fileRouter.use(bodyParser.json());

fileRouter.route('/upload')
    .get(authenticate.verifyToken, (request, response, next) => {
        response.statusCode = 403;
        response.end('GET operation not supported on /files/upload');
    })
    .post(authenticate.verifyToken, upload.single('filename'), (request, response, next) => {
        Files.create({filename: request.file.filename, size: request.file.size, mimetype: request.file.mimetype})
            .then((file) => {
                console.log("File uploaded! ", file)
                response.statusCode = 200;
                response.setHeader('Content-Type', 'application/json');
                response.json(request.file);
            }, (err) => next(err)).catch((err) => next(err));
    })
    .put(authenticate.verifyToken, (request, response, next) => {
        response.statusCode = 403;
        response.end('PUT operation not supported on /files/upload');
    })
    .delete(authenticate.verifyToken, (request, response, next) => {
        response.statusCode = 403;
        response.end('DELETE operation not supported on /files/upload');
    });

module.exports = fileRouter;
