const express = require('express');
const bodyParser = require('body-parser');
const authenticate = require('../authenticate');
const multer = require('multer');
const mime = require('mime');
const fs = require('fs');
const path = require('path');

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
    if (!file.originalname.match(/\.(jpg|jpeg|png|gif|mp3|mp4)$/)) {
        return callback(new Error('You may only upload media'), null);
    }
    callback(null, true);
};

const upload = multer({storage: storage, fileFilter: staticFileFilter});

const fileRouter = express.Router();
fileRouter.use(bodyParser.json());

fileRouter.route('/')
    .get(authenticate.verifyToken, (request, response, next) => {
        response.statusCode = 403;
        response.end('GET operation not supported on /files');
    })
    .post(authenticate.verifyToken, (request, response, next) => {
        response.statusCode = 403;
        response.end('POST operation not supported on /files');
    })
    .put(authenticate.verifyToken, (request, response, next) => {
        response.statusCode = 403;
        response.end('PUT operation not supported on /files');
    })
    .delete(authenticate.verifyToken, authenticate.verifyAdmin, (request, response, next) => {
        Files.remove({}).then((resp) => {
            response.statusCode = 200;
            response.setHeader('Content-Type', 'application/json');
            response.json(resp);
        }, (err) => next(err)).catch((err) => next(err));
    })

fileRouter.route('/upload')
    .get(authenticate.verifyToken, (request, response, next) => {
        response.statusCode = 403;
        response.end('GET operation not supported on /files/upload');
    })
    .post(authenticate.verifyToken, upload.single('filename'), (request, response, next) => {
        Files.create({filename: request.file.filename, size: request.file.size, mimetype: request.file.mimetype})
            .then((file) => {
                console.log("File uploaded! ", file)
                let newPath = "public\\storage\\" + file._id + "."  + mime.getExtension(file.mimetype);
                fs.rename(request.file.path, newPath, (err) => { if (err) next(err) });
                response.statusCode = 200;
                response.setHeader('Content-Type', 'application/json');
                response.json({
                    filename: request.file.originalname,
                    mimetype: request.file.mimetype,
                    size: request.file.size,
                    status: "success",
                    url: file._id
                });
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

fileRouter.route('/:fileId')
    .get((request, response, next) => {
        response.sendFile(path.join(__dirname, '..', 'public', 'filepage.html'));
    })
    .post(authenticate.verifyToken, (request, response, next) => {
        response.statusCode = 403;
        response.end('POST operation not supported on /files/:fileId');
    })
    .put(authenticate.verifyToken, (request, response, next) => {
        response.statusCode = 403;
        response.end('PUT operation not supported on /files/:fileId');
    })
    .delete();

fileRouter.route('/:fileId/download')
    .get((request, response, next) => {
        Files.findById(request.params.fileId).then((file) => {
            filename = file._id + "." + mime.getExtension(file.mimetype);
            publicPath = path.resolve(__dirname, '../public/storage')
            response.setHeader('Content-Disposition',
                `attachment; filename=${file.filename}`); // Download the file as its original name
            response.sendFile(filename, {root: publicPath});
        }, (err) => {
            if (err.name === 'CastError' && err.kind === 'ObjectId') {
                return response.status(400).send({ message: 'Invalid ObjectId' });
            }
        }).catch((err) => next(err));
    })
    .post(authenticate.verifyToken, (request, response, next) => {
        response.statusCode = 403;
        response.end('POST operation not supported on /files/:fileId');
    })
    .put(authenticate.verifyToken, (request, response, next) => {
        response.statusCode = 403;
        response.end('PUT operation not supported on /files/:fileId');
    })
    .delete();

module.exports = fileRouter;
