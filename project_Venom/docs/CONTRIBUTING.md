# 🎯 Best Practices & Contributing Guide

Guidelines for using, extending, and contributing to Project Venom.

## 📚 Table of Contents

1. [Code Quality](#code-quality)
2. [Git Workflow](#git-workflow)
3. [Security](#security)
4. [Performance](#performance)
5. [Documentation](#documentation)
6. [Testing](#testing)
7. [Contributing](#contributing)

---

## Code Quality

### Style Guidelines

**Python Code Style (PEP 8):**

```python
# Good: Clear, readable code
def analyze_image(image_path: str) -> dict:
    """
    Analyze an image for objects using YOLO.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Dictionary with detected objects and confidence scores
    """
    vision = VisionSystem()
    return vision.analyze_frame(image_path)

# Avoid: Unclear, hard to maintain
def ai(x):
    v = VisionSystem()
    return v.analyze_frame(x)
```

### Type Hints

Always use type hints for function arguments and return values:

```python
# Good
def process_query(query: str) -> str:
    pass

# Avoid
def process_query(query):
    pass
```

### Docstrings

Use comprehensive docstrings:

```python
def send_whatsapp(target: str, message: str) -> bool:
    """
    Send a WhatsApp message to a contact.
    
    Args:
        target: Contact name or phone number
        message: Message text to send
        
    Returns:
        True if successful, False otherwise
        
    Raises:
        ValueError: If target is not found
        
    Example:
        >>> send_whatsapp("John", "Hello!")
        True
    """
    pass
```

### Linting & Formatting

```bash
# Format code with Black
black . --line-length=120

# Lint with Pylint
pylint **/*.py

# Type checking with mypy
mypy .
```

---

## Git Workflow

### Branch Naming

```
feature/description          # New features
bugfix/description          # Bug fixes
docs/description            # Documentation
refactor/description        # Code refactoring
test/description            # Test additions
chore/description           # Maintenance tasks
```

### Commit Messages

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting, missing semicolons)
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Test additions
- `chore`: Build, dependencies, tooling

**Examples:**

```
feat(vision): add multi-model detection support

Implement support for running multiple YOLO models
simultaneously for improved accuracy. Uses async processing
to prevent blocking.

Closes #123

---

fix(api): handle timeout on external API calls

Wrap API calls in try-catch with exponential backoff.
Default timeout set to 30 seconds.

---

docs(setup): add Docker deployment guide

Added comprehensive Docker and docker-compose setup
instructions including production configuration.
```

### Pull Request Workflow

1. **Create branch from `main`:**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/my-feature
   ```

2. **Make changes with meaningful commits**

3. **Push and create PR:**
   ```bash
   git push origin feature/my-feature
   ```

4. **Describe PR clearly:**
   - What problem does it solve?
   - How does it solve it?
   - Any breaking changes?
   - Testing done?

5. **Wait for review and address feedback**

6. **Squash and merge when approved**

---

## Security

### API Key Management

✅ **DO:**
```python
# Use environment variables
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY not set")
```

❌ **DON'T:**
```python
# Never hardcode keys
api_key = "AIzaSyDTbMQHKP9XCvn2vueSVJk_9V6ummsriHg"
```

### Credential Storage

✅ **DO:**
- Use `.env` files (excluded from git)
- Use environment variables in production
- Use Kubernetes secrets for containerized deployments

❌ **DON'T:**
- Commit `.env` files
- Log sensitive data
- Pass credentials as function parameters

### Data Protection

```python
# Sanitize user inputs
def safe_query(query: str) -> str:
    # Remove potentially dangerous characters
    query = query.replace(';', '').replace('`', '')
    return query

# Don't log sensitive data
logger.info(f"Processing query: {query}")  # OK
logger.info(f"API Key: {api_key}")  # NEVER do this
```

---

## Performance

### Optimization Tips

**1. Use Async/Await:**
```python
# Good: Non-blocking
async def process_multiple_images(images: list) -> list:
    tasks = [vision.analyze_frame(img) for img in images]
    return await asyncio.gather(*tasks)

# Bad: Blocking
def process_multiple_images(images: list) -> list:
    return [vision.analyze_frame(img) for img in images]
```

**2. Cache Results:**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_operation(param: str) -> str:
    # This will be cached for repeated calls
    return do_work(param)
```

**3. Batch Operations:**
```python
# Good: Batch processing
results = model.predict_batch(images)

# Bad: Loop processing
results = [model.predict(img) for img in images]
```

**4. Monitor Performance:**
```bash
# Use Python profiler
python -m cProfile -s cumtime main.py

# Check memory usage
python -m memory_profiler script.py

# Use built-in analytics
python -m modules.analytics
```

---

## Documentation

### README Standards

Every module should have clear documentation:

```python
"""
Vision Module - Advanced visual processing with YOLOv8

This module provides real-time object detection, scene analysis,
and image classification capabilities using the YOLOv8 model.

Features:
    - Real-time webcam streaming
    - CUDA GPU acceleration
    - Multi-object detection
    - Scene understanding

Example:
    >>> vision = VisionSystem()
    >>> results = vision.analyze_frame('image.jpg')
    >>> print(results)
    "I can see: 2 person(s), 1 laptop(s)"

Note:
    Requires YOLO model weights (auto-downloaded on first run)
"""
```

### Documentation Files

Create `.md` files for complex features:
- `docs/ARCHITECTURE.md` - System design
- `docs/API.md` - API reference
- `docs/DEPLOYMENT_GUIDE.md` - Setup instructions
- `docs/TROUBLESHOOTING.md` - Common issues

---

## Testing

### Test Structure

```python
# tests/test_vision.py

import pytest
from modules.vision import VisionSystem

class TestVisionSystem:
    """Tests for VisionSystem module"""
    
    @pytest.fixture
    def vision(self):
        """Create VisionSystem instance"""
        return VisionSystem()
    
    def test_initialization(self, vision):
        """Test system initializes correctly"""
        assert vision.active is True
    
    def test_analyze_frame_returns_string(self, vision):
        """Test analyze_frame returns string result"""
        result = vision.analyze_frame()
        assert isinstance(result, str)
    
    def test_analyze_frame_with_path(self, vision):
        """Test analyze_frame with image path"""
        result = vision.analyze_frame("test_image.jpg")
        assert result is not None
    
    @pytest.mark.skip(reason="Requires camera")
    def test_webcam_stream(self, vision):
        """Test webcam streaming functionality"""
        pass
```

### Running Tests

```bash
# Run all tests
pytest -v

# Run specific test file
pytest tests/test_vision.py -v

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test function
pytest tests/test_vision.py::TestVisionSystem::test_initialization -v
```

---

## Contributing

### Step-by-Step Guide

**1. Fork & Clone:**
```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR_USERNAME/jarvis_training.git
cd project_Venom
git remote add upstream https://github.com/Karn0511/jarvis_training.git
```

**2. Create Feature Branch:**
```bash
git checkout -b feature/my-feature
```

**3. Make Changes:**
- Write clean, documented code
- Add/update tests
- Update documentation
- Follow style guidelines

**4. Test Your Changes:**
```bash
pytest -v
black . --line-length=120
pylint **/*.py
```

**5. Commit with Good Messages:**
```bash
git add .
git commit -m "feat(module): clear description of changes"
```

**6. Push to Your Fork:**
```bash
git push origin feature/my-feature
```

**7. Create Pull Request:**
- Go to GitHub
- Click "Compare & pull request"
- Describe your changes
- Reference related issues

**8. Address Review Feedback:**
```bash
# Make requested changes
git add .
git commit -m "Address review feedback"
git push origin feature/my-feature
```

### Code Review Checklist

- [ ] Code follows style guidelines
- [ ] Type hints are present
- [ ] Docstrings are comprehensive
- [ ] Tests are added/updated
- [ ] Documentation is updated
- [ ] No hardcoded secrets
- [ ] Performance is reasonable
- [ ] Error handling is proper

---

## Resources

- **Python Style Guide**: https://pep8.org/
- **Git Best Practices**: https://git-scm.com/book/
- **Async Python**: https://docs.python.org/3/library/asyncio.html
- **Testing**: https://docs.pytest.org/
- **Type Hints**: https://docs.python.org/3/library/typing.html

---

**Thank you for contributing to Project Venom!**

Questions? Open an issue or contact the maintainers.
