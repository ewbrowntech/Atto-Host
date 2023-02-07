const fs = require('fs');
const path = require('path');

exports.clearStorage = (storageDir) => {
    fs.readdir(storageDir, (err, files) => {
        if (err) throw err;

        for (const file of files) {
            fs.unlink(path.join(storageDir, file), (err) => {
                if (err) throw err;
            });
        }
    });
}