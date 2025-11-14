# Interactive Video Avatar Implementation Guide

## Overview

This document describes the three interactive video avatar options implemented for Talk to Jesus AI:

1. **AI-Generated Video Avatar** - Photorealistic talking avatar with lip-sync
2. **Live Video Streaming** - Real-time video communication interface
3. **Animated 3D Avatar** - Browser-based 3D character animation

---

## Option 1: AI-Generated Video Avatar

### Features
- Photorealistic Jesus avatar with natural lip-syncing
- Text-to-video generation from AI responses
- Support for multiple AI video services (D-ID, Synthesia, HeyGen)
- Fallback to static image with audio when service unavailable

### Services Supported

#### D-ID (Recommended)
- **Cost**: ~$0.10-0.30 per minute
- **Quality**: Excellent lip-sync and natural movements
- **Latency**: 10-30 seconds per video
- **API**: REST API with webhook support

#### Synthesia
- **Cost**: Subscription-based ($30/month minimum)
- **Quality**: Professional studio-quality videos
- **Latency**: 30-60 seconds per video
- **API**: REST API

#### HeyGen
- **Cost**: ~$24/month for API access
- **Quality**: High-quality realistic avatars
- **Latency**: 15-45 seconds per video
- **API**: REST API

### Setup Instructions

#### 1. Get API Credentials

**For D-ID:**
1. Sign up at https://www.d-id.com/
2. Get your API key from the dashboard
3. Set environment variable: `D_ID_API_KEY=your_key_here`

**For Synthesia:**
1. Sign up at https://www.synthesia.io/
2. Get API credentials from account settings
3. Set environment variable: `SYNTHESIA_API_KEY=your_key_here`

#### 2. Configure Avatar Settings

Edit `config/avatar_config.json`:

```json
{
  "service": "d-id",
  "avatar": {
    "source_url": "https://example.com/jesus-avatar.jpg",
    "voice_id": "en-US-neural2-j",
    "style": "natural"
  },
  "fallback": {
    "enabled": true,
    "image": "static/images/jesus-fallback.jpg",
    "audio_only": true
  }
}
```

#### 3. Environment Variables

```bash
# Required
D_ID_API_KEY=your_d_id_api_key_here
SYNTHESIA_API_KEY=your_synthesia_key_here

# Optional
VIDEO_AVATAR_SERVICE=d-id  # or 'synthesia', 'heygen'
VIDEO_CACHE_ENABLED=true
VIDEO_CACHE_DIR=/tmp/video_cache
```

### API Endpoints

#### Generate Video Avatar Response
```
POST /api/video/generate
```

**Request:**
```json
{
  "text": "Peace be with you, my child. How may I help you today?",
  "voice_settings": {
    "speed": 1.0,
    "emotion": "calm"
  }
}
```

**Response:**
```json
{
  "video_url": "https://cdn.d-id.com/videos/abc123.mp4",
  "duration": 5.2,
  "status": "ready",
  "thumbnail": "https://cdn.d-id.com/thumbnails/abc123.jpg"
}
```

#### Stream Video Avatar
```
GET /api/video/stream/{video_id}
```

### Usage in Frontend

```javascript
// Request video generation
async function generateVideoResponse(message) {
    const response = await fetch('/api/video/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({text: message})
    });
    
    const data = await response.json();
    
    // Display video
    const videoElement = document.getElementById('avatar-video');
    videoElement.src = data.video_url;
    videoElement.play();
}
```

---

## Option 2: Live Video Streaming Interface

### Features
- Real-time WebRTC video communication
- Integration with Zoom, Google Meet, or custom WebRTC
- Screen sharing and recording capabilities
- Low-latency audio/video streaming

### Setup Instructions

#### 1. WebRTC Configuration

```bash
# STUN/TURN servers for peer connection
WEBRTC_STUN_SERVER=stun:stun.l.google.com:19302
WEBRTC_TURN_SERVER=turn:your-turn-server.com
WEBRTC_TURN_USERNAME=your_username
WEBRTC_TURN_PASSWORD=your_password
```

#### 2. Zoom Integration

```bash
ZOOM_API_KEY=your_zoom_api_key
ZOOM_API_SECRET=your_zoom_secret
ZOOM_SDK_KEY=your_sdk_key
ZOOM_SDK_SECRET=your_sdk_secret
```

### API Endpoints

#### Create Video Session
```
POST /api/video/session/create
```

#### Join Video Session
```
GET /api/video/session/{session_id}/join
```

---

## Option 3: Animated 3D Avatar

### Features
- Browser-based 3D rendering (Three.js/Babylon.js)
- Real-time animation based on text input
- Customizable avatar appearance
- No external API required - runs client-side

### Technologies
- **Three.js**: 3D rendering
- **Rhubarb Lip Sync**: Automatic lip-sync generation
- **Ready Player Me**: Avatar creation (optional)

### Setup Instructions

#### 1. Install Dependencies

```bash
npm install three @mediapipe/holistic rhubarb-lip-sync
```

#### 2. Configure Avatar Model

Place 3D model files in `static/models/`:
- `jesus_avatar.glb` - Main 3D model (GLTF/GLB format)
- `jesus_avatar_animations.json` - Animation data

### API Endpoints

#### Load 3D Avatar
```
GET /api/avatar/3d/load
```

#### Animate Avatar
```
POST /api/avatar/3d/animate
```

**Request:**
```json
{
  "text": "Peace be with you",
  "animation": "talking",
  "emotion": "calm"
}
```

---

## Performance Comparison

| Feature | AI Video | Live Streaming | 3D Avatar |
|---------|----------|----------------|-----------|
| Latency | 10-60s | <100ms | <1s |
| Quality | Excellent | Depends on connection | Good |
| Cost | $0.10-0.30/min | $0-$20/month | Free |
| Bandwidth | Low (pre-generated) | High (streaming) | Medium |
| Offline | Yes (cached) | No | Yes |

---

## Troubleshooting

### AI Video Avatar Issues

**Problem**: Video generation fails
- Check API key is valid
- Verify account has credits
- Check rate limits haven't been exceeded

**Problem**: Video takes too long to generate
- Use shorter text (< 200 words)
- Enable video caching
- Consider pre-generating common responses

### Live Streaming Issues

**Problem**: Video connection fails
- Check firewall allows WebRTC ports
- Verify STUN/TURN servers are accessible
- Test with different browsers

### 3D Avatar Issues

**Problem**: Avatar doesn't load
- Check browser supports WebGL
- Verify 3D model files are accessible
- Check console for errors

---

## Cost Estimates

### Monthly Usage: 1000 conversations

**AI Video Avatar (D-ID)**
- Average 3 min per conversation
- 3000 minutes × $0.15 = **$450/month**

**Live Streaming (Twilio)**
- Average 10 min per conversation
- 10000 minutes × $0.0015 = **$15/month**

**3D Avatar**
- No per-usage costs
- Hosting costs only = **$5/month**

---

## Recommendations

1. **Start with 3D Avatar** - Free, fast, and works offline
2. **Add AI Video** for special features - Premium experience
3. **Use Live Streaming** for real-time pastoral care

## Next Steps

1. Choose which option(s) to implement
2. Obtain necessary API keys
3. Configure environment variables
4. Test in development environment
5. Deploy to production with monitoring
