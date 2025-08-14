# MongoDB Atlas Setup Guide

## Prerequisites
1. A MongoDB Atlas account (free tier available)
2. Python 3.7+ installed
3. Your Flask application

## Step 1: Create MongoDB Atlas Cluster

1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas) and sign up/login
2. Create a new project
3. Build a new cluster (free tier: M0)
4. Choose your preferred cloud provider and region
5. Click "Create Cluster"

## Step 2: Set Up Database Access

1. In the left sidebar, click "Database Access"
2. Click "Add New Database User"
3. Choose "Password" authentication
4. Create a username and password (save these!)
5. Set privileges to "Read and write to any database"
6. Click "Add User"

## Step 3: Set Up Network Access

1. In the left sidebar, click "Network Access"
2. Click "Add IP Address"
3. For development: Click "Allow Access from Anywhere" (0.0.0.0/0)
4. For production: Add your specific IP addresses
5. Click "Confirm"

## Step 4: Get Connection String

1. Go back to "Database" in the left sidebar
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string

## Step 5: Configure Your Application

1. Create a `.env` file in your project root:
```bash
# Flask Secret Key
SECRET_KEY=your-secret-key-here

# MongoDB Atlas Connection String
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/instagram_facebook_app?retryWrites=true&w=majority
```

2. Replace the placeholders:
   - `username`: Your database username
   - `password`: Your database password
   - `cluster`: Your cluster name
   - `instagram_facebook_app`: Your database name

## Step 6: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 7: Test Connection

Run your Flask application:
```bash
python app.py
```

You should see: "Connected to MongoDB Atlas successfully!"

## Troubleshooting

### Connection Issues
- Verify your IP address is whitelisted
- Check username/password are correct
- Ensure cluster is running
- Check network connectivity

### Common Errors
- `ServerSelectionTimeoutError`: Network/authentication issue
- `AuthenticationFailed`: Wrong username/password
- `OperationFailure`: Insufficient privileges

## Security Notes

1. Never commit your `.env` file to version control
2. Use strong passwords for database users
3. Restrict IP access in production
4. Regularly rotate database credentials

## Production Considerations

1. Use environment-specific connection strings
2. Implement connection pooling
3. Set up monitoring and alerts
4. Regular backups
5. Use VPC peering for enhanced security
