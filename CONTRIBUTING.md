# Contributing

Thank you for your interest in contributing to the txtai RAG system!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/ragaws.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Commit: `git commit -m "Add your feature"`
6. Push: `git push origin feature/your-feature-name`
7. Open a Pull Request

## Code Style

### Python (Backend)

- Follow PEP 8
- Use type hints where possible
- Maximum line length: 100 characters
- Use `black` for formatting: `black app/`

### JavaScript (Frontend)

- Follow ESLint rules
- Use Prettier for formatting: `npm run format`
- Use functional components with hooks

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage

## Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Update API documentation if endpoints change

## Commit Messages

Use clear, descriptive commit messages:

```
feat: Add support for DOCX file uploads
fix: Resolve EFS mount issue in ECS tasks
docs: Update deployment guide with ALB setup
refactor: Decouple retrieval and generation layers
```

## Pull Request Process

1. Ensure your code follows the style guide
2. Add tests for new functionality
3. Update documentation as needed
4. Ensure all CI checks pass
5. Request review from maintainers

## Questions?

Open an issue for questions or discussions.

