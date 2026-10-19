const express = require('express'); // Express app
const router = express.Router(); // Router logic
const jwt = require('jsonwebtoken'); // Enable JSON web tokens

// This is where we import the controllers we will route
const tripsController = require("../controllers/trips");
const authController = require("../controllers/authentication");

// Method to authenticate our JWT
function authenticateJWT(req, res, next) {
    const authHeader = req.get('authorization');
    const [scheme, token, ...extraParts] = (authHeader || '').trim().split(/\s+/);

    if (scheme?.toLowerCase() !== 'bearer' || !token || extraParts.length > 0) {
        return res.status(401).json({ message: 'A valid bearer token is required.' });
    }

    if (!process.env.JWT_SECRET) {
        return res.status(500).json({ message: 'Authentication is not configured.' });
    }

    jwt.verify(token, process.env.JWT_SECRET, (err, verified) => {
        if (err || !verified) {
            return res.status(401).json({ message: 'The token is invalid or expired.' });
        }

        req.auth = verified;
        return next();
    });
}

// define route for registration endpoint
router
    .route('/register')
    .post(authController.register);

// define route for login endpoint
router
    .route('/login')
    .post(authController.login);

// define route for our trips endpoint
router
    .route('/trips')
    .get(tripsController.tripsList)
    .post(authenticateJWT, tripsController.tripsAddTrip);

// GET Method routes tripsFindByCode - requires parameter
router
    .route('/trips/:tripCode')
    .get(tripsController.tripsFindByCode) 
    .put(authenticateJWT, tripsController.tripsUpdateTrip);

module.exports = router;
