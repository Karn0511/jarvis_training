"""
Jarvis Backend Client
Handles all communication with backend service
"""

import requests
import os
from typing import Dict, Any, Optional, List

class JarvisClient:
    """Advanced client for Jarvis backend with retry logic"""

    def __init__(self):
        self.base_url = os.getenv('JARVIS_BACKEND_URL', 'http://127.0.0.1:8574')
        self.timeout = 30
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Jarvis-CLI/2.0',
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method,
                url,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            raise Exception(
                "Cannot connect to backend. Is it running?\n"
                "Start with: cd backend && uvicorn main:app"
            )
        except requests.exceptions.Timeout:
            raise Exception("Request timed out. Backend is taking too long to respond.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def ping(self) -> dict:
        """Check backend health"""
        import time
        start = time.time()
        response = self._request('GET', '/')
        response_time = int((time.time() - start) * 1000)
        response['response_time'] = response_time
        return response

    def ask(self, question: str, context: Optional[List[dict]] = None) -> dict:
        """Ask a question"""
        payload = {
            'message': question,
            'stream': False
        }
        if context:
            payload['context'] = context
        
        return self._request('POST', '/api/chat', json=payload)

    def analyze_code(self, code: str, filename: str) -> dict:
        """Analyze code"""
        # Detect language from filename
        ext_to_lang = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust',
        }
        
        ext = os.path.splitext(filename)[1]
        language = ext_to_lang.get(ext, 'python')
        
        return self._request('POST', '/api/analyze', json={
            'code': code,
            'language': language,
            'filename': filename
        })

    def execute(self, command: str) -> dict:
        """Execute shell command"""
        return self._request('POST', '/api/execute', json={'command': command})
    
    def refactor_code(self, code: str, language: str) -> dict:
        """Refactor code"""
        return self._request('POST', '/api/refactor', json={
            'code': code,
            'language': language
        })

