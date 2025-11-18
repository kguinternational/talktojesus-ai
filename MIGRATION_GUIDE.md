# 🔄 Migration Guide: Flask to FastAPI (2025 Upgrade)

## Quick Start - Test the New Version

### 1. Install New Dependencies
```bash
pip install fastapi[all] uvicorn openai
```

### 2. Set OpenAI API Key (Optional but Recommended)
```bash
export OPENAI_API_KEY="your-key-here"
# or add to .env file
```

### 3. Run New FastAPI Version
```bash
# Using uvicorn directly
uvicorn app_fastapi_2025:app --reload --port 8000

# Or using Python
python3 app_fastapi_2025.py
```

### 4. Access the Application
- **Homepage**: http://localhost:8000
- **Interactive API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## Test New Features

### Test REST API
```bash
# Chat endpoint
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"text": "I need guidance about forgiveness"}'

# Prayer endpoint
curl -X POST "http://localhost:8000/api/prayer" \
  -H "Content-Type: application/json" \
  -d '{"prayer_text": "Please help me find peace", "name": "John"}'

# Streaming response
curl "http://localhost:8000/api/chat/stream?message=Tell%20me%20about%20love"
```

### Test WebSocket (Real-Time Chat)
Create `test_websocket.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Test</title>
</head>
<body>
    <h1>Real-Time Chat Test</h1>
    <input id="messageInput" type="text" placeholder="Type message...">
    <button onclick="sendMessage()">Send</button>
    <div id="messages"></div>

    <script>
        const ws = new WebSocket('ws://localhost:8000/ws/chat');
        
        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            document.getElementById('messages').innerHTML += 
                '<p><strong>Jesus:</strong> ' + data.response + '</p>';
        };
        
        function sendMessage() {
            const input = document.getElementById('messageInput');
            ws.send(JSON.stringify({message: input.value}));
            document.getElementById('messages').innerHTML += 
                '<p><strong>You:</strong> ' + input.value + '</p>';
            input.value = '';
        }
    </script>
</body>
</html>
```

---

## Key Differences: Flask vs FastAPI

| Feature | Flask (Old) | FastAPI (New) |
|---------|------------|---------------|
| **Performance** | 2,000 req/sec | 15,000 req/sec |
| **Async Support** | ❌ Manual (complicated) | ✅ Built-in |
| **Type Safety** | ❌ Optional | ✅ Required (Pydantic) |
| **Auto Docs** | ❌ Manual (Swagger extension) | ✅ Automatic |
| **Validation** | ❌ Manual | ✅ Automatic (Pydantic) |
| **WebSocket** | ❌ Needs extensions | ✅ Built-in |
| **Startup** | `app.run()` | `uvicorn app:app` |
| **Request Model** | `request.get_json()` | `MessageRequest` model |
| **Error Handling** | Manual try/catch | Automatic validation errors |

---

## Code Comparison

### Before (Flask)
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'Text required'}), 400
    
    # Process...
    response = generate_response(text)
    return jsonify({'response': response})
```

### After (FastAPI)
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class MessageRequest(BaseModel):
    text: str

@app.post("/api/chat")
async def chat(request: MessageRequest):
    # Type-safe, auto-validated, documented!
    response = await generate_response(request.text)
    return {"response": response}
```

---

## Migration Checklist

### Step 1: Update Dependencies
- [ ] Install FastAPI and uvicorn
- [ ] Install OpenAI SDK (optional)
- [ ] Install async PostgreSQL driver if using DB

### Step 2: Convert Routes
- [ ] Change `@app.route()` to `@app.get()/@app.post()`
- [ ] Add `async` to all handler functions
- [ ] Create Pydantic models for request/response
- [ ] Replace `request.get_json()` with model parameters

### Step 3: Update Database Calls
- [ ] Replace synchronous DB calls with async
- [ ] Use `asyncpg` instead of `psycopg2`
- [ ] Add `await` to all DB queries

### Step 4: Add New Features
- [ ] Implement WebSocket endpoints
- [ ] Add streaming responses
- [ ] Integrate OpenAI GPT-4
- [ ] Add Prometheus metrics

### Step 5: Testing
- [ ] Test all endpoints with `/docs`
- [ ] Load test with `locust` or `hey`
- [ ] Test WebSocket connections
- [ ] Verify OpenAI integration

### Step 6: Deployment
- [ ] Update Dockerfile for FastAPI
- [ ] Use `uvicorn` instead of `gunicorn`
- [ ] Update docker-compose
- [ ] Deploy to production

---

## Performance Benchmarking

### Before (Flask)
```bash
# Install apache bench
sudo apt-get install apache2-utils

# Test Flask app
ab -n 1000 -c 10 http://localhost:5000/health
```

### After (FastAPI)
```bash
# Test FastAPI app
ab -n 1000 -c 10 http://localhost:8000/health
```

Expected improvement: **5-7x faster response times**

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fastapi'"
**Solution**: Install dependencies
```bash
pip install fastapi[all] uvicorn
```

### Issue: "OpenAI API key not found"
**Solution**: Set environment variable
```bash
export OPENAI_API_KEY="sk-..."
```

### Issue: "Port 8000 already in use"
**Solution**: Use different port
```bash
uvicorn app_fastapi_2025:app --port 8001
```

### Issue: WebSocket connection fails
**Solution**: Check CORS settings
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Next Steps

1. **Test Both Versions**: Run Flask and FastAPI side-by-side
2. **Gradual Migration**: Move endpoints one at a time
3. **Monitor Performance**: Compare response times
4. **User Feedback**: Test with real users
5. **Full Migration**: Switch to FastAPI completely

---

## Resources

- FastAPI Documentation: https://fastapi.tiangolo.com/
- Migration Tutorial: https://testdriven.io/blog/fastapi-flask/
- OpenAI API: https://platform.openai.com/docs
- Uvicorn: https://www.uvicorn.org/

---

## Questions?

Check out the `/docs` endpoint in FastAPI - it has interactive API documentation where you can test all endpoints directly in your browser!
