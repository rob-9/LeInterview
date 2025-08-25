# LeInterview

An AI-powered mock interview platform that provides real-time feedback on technical and behavioral interviews.

## 🚀 Features

- **🎤 Real-time Speech Recognition**: Records and transcribes your responses during interviews
- **🤖 AI Feedback**: Provides instant feedback on your interview performance using Google's Gemini AI
- **💻 Code Execution**: Execute and test code in Python, Java, C++, and JavaScript directly in the browser
- **🏢 Company-specific Questions**: Get interview questions tailored to specific companies
- **📱 Responsive UI**: Modern, responsive interface optimized for all devices
- **🔒 Secure**: No hardcoded API keys, proper environment variable management

## 🛠️ Quick Start

### Automated Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd LeInterview
```

2. Run the setup script:
```bash
python setup.py
```

3. Edit `.env` file and add your GEMINI_API_KEY

4. Start the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Manual Setup

#### Prerequisites

- Python 3.8+
- GCC/G++ compilers
- Java JDK (for Java code execution)
- Audio drivers (for speech recognition)

#### Installation Steps

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

3. Run the application:
```bash
python app.py
```

## 🌐 Deployment

For production deployment, see [deploy.md](deploy.md) for detailed instructions on:
- Heroku deployment
- Docker deployment  
- Railway deployment
- Vercel deployment
- Custom server deployment

## 📋 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Your Google Gemini API key | ✅ Yes |
| `FLASK_ENV` | Environment (development/production) | ❌ No |
| `FLASK_DEBUG` | Enable debug mode | ❌ No |
| `PORT` | Server port (auto-set by platforms) | ❌ No |

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page |
| GET | `/interview` | Interview page |
| POST | `/start-interview` | Start interview session |
| POST | `/stop-interview` | Stop interview session |
| GET | `/get-feedback` | Get AI feedback on responses |
| POST | `/execute` | Execute code in various languages |
| GET | `/random-quest/<company_name>` | Get company-specific questions |

## 📁 Project Structure

```
LeInterview/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies  
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── setup.py              # Automated setup script
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── Procfile              # Heroku deployment file
├── runtime.txt           # Python runtime version
├── wsgi.py               # WSGI entry point
├── templates/            # HTML templates
│   ├── index.html        # Landing page
│   ├── interview.html    # Interview interface
│   └── companies.txt     # Company questions database
└── static/               # Static assets
    └── Welcome.png       # Welcome image
```

## 🧪 Testing

To test the application:

1. **Speech Recognition**: Click "Start Recording" and speak
2. **AI Feedback**: Verify feedback appears in the feedback panel
3. **Code Execution**: Write code in the editor and click "Run Code"
4. **Question Generation**: Click "New Question" to get company-specific questions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the [deployment guide](deploy.md)
2. Ensure all environment variables are set correctly
3. Verify system dependencies are installed
4. Check the console/logs for error messages

## 🔮 Roadmap

- [ ] Add more programming languages
- [ ] Implement video interview features
- [ ] Add interview analytics dashboard
- [ ] Support for multiple AI models
- [ ] Mobile app version