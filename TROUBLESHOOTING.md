# Troubleshooting Guide

## "Nothing happens when I access localhost:5000"

If you're unable to access the application at http://localhost:5000, follow these steps:

### Step 1: Check if the Application is Running

1. Open a terminal/command prompt
2. Navigate to the project directory:
   ```bash
   cd talktojesus-ai
   ```

3. Check if Python is installed:
   ```bash
   python3 --version
   ```
   You should see Python 3.8 or higher. If not, install Python first.

### Step 2: Install Dependencies

```bash
pip3 install -r requirements.txt
```

### Step 3: Start the Application

**Option A: Use the launch script (Recommended)**
```bash
./run.sh
```

**Option B: Run directly**
```bash
python3 app.py
```

You should see output like:
```
* Serving Flask app 'app'
* Running on http://127.0.0.1:5000
* Running on http://10.x.x.x:5000
```

### Step 4: Access the Application

Once you see "Running on http://127.0.0.1:5000", open your web browser and go to:
- http://localhost:5000
- OR http://127.0.0.1:5000

### Common Issues and Solutions

#### Issue 1: Port 5000 Already in Use
**Error:** "Address already in use"

**Solution:** Another application is using port 5000. Use a different port:
```bash
PORT=8080 python3 app.py
```
Then access at http://localhost:8080

#### Issue 2: Python Not Found
**Error:** "python3: command not found"

**Solution:** Install Python 3.8 or higher:
- **macOS:** `brew install python3`
- **Ubuntu/Debian:** `sudo apt-get install python3 python3-pip`
- **Windows:** Download from https://www.python.org/downloads/

#### Issue 3: Dependencies Not Installed
**Error:** "ModuleNotFoundError: No module named 'flask'"

**Solution:** Install dependencies:
```bash
pip3 install -r requirements.txt
```

#### Issue 4: Permission Denied on run.sh
**Error:** "Permission denied: ./run.sh"

**Solution:** Make the script executable:
```bash
chmod +x run.sh
./run.sh
```

#### Issue 5: Firewall Blocking Connection
**Solution:** 
- Check your firewall settings
- Temporarily disable firewall to test
- Add exception for Python or port 5000

#### Issue 6: Application Starts but Browser Shows "Connection Refused"
**Possible causes:**
1. Application hasn't finished starting - wait 5-10 seconds
2. Check if the application is binding to the correct address
3. Try using 127.0.0.1 instead of localhost: http://127.0.0.1:5000

### Verify Application is Running

Check if the application is listening on port 5000:

**On macOS/Linux:**
```bash
lsof -i :5000
```

**On Windows:**
```bash
netstat -ano | findstr :5000
```

### Debug Mode

To see detailed error messages, enable debug mode:
```bash
FLASK_DEBUG=True python3 app.py
```

### Check Application Logs

The application logs will show in the terminal where you started it. Look for:
- ✅ "Running on http://..." means it's working
- ❌ Any error messages indicate what's wrong

## Need More Help?

If you're still having issues:

1. **Check the logs** - Error messages in the terminal output
2. **Verify Python version** - Must be 3.8 or higher
3. **Check dependencies** - Run `pip3 list | grep -i flask`
4. **Try a different browser** - Sometimes browser cache causes issues
5. **Restart your computer** - Fixes many network-related issues

## Quick Test Commands

Run these to verify everything is working:

```bash
# Test if app can start
python3 -c "import flask; print('Flask OK')"

# Test if port is available
python3 -c "import socket; s=socket.socket(); s.bind(('', 5000)); print('Port 5000 available')"

# Start app with verbose output
FLASK_DEBUG=True python3 app.py
```

## Docker Information

**Q: Is this hosted in Docker?**

**A:** No, this application is not currently containerized with Docker. It runs directly as a Python Flask application.

However, if you'd like to run it in Docker, you can create a Dockerfile (see DOCKER.md for instructions).
