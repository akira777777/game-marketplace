# Task Completion Checklist

## When a Development Task is Complete

### Code Quality Checks
- [ ] **Format code**: Run `black app/` and `isort app/`
- [ ] **Lint code**: Run `flake8 app/` and fix any issues
- [ ] **Type checking**: Ensure all functions have proper type hints
- [ ] **Documentation**: Add/update docstrings for new functions and classes

### Testing
- [ ] **Unit tests**: Write or update tests for new functionality
- [ ] **Integration tests**: Test API endpoints if modified
- [ ] **Manual testing**: Test the functionality manually
- [ ] **Run test suite**: Execute `pytest` to ensure all tests pass

### Database Changes
- [ ] **Migrations**: Create migration if database schema changed
- [ ] **Test migrations**: Ensure migrations run cleanly
- [ ] **Backup consideration**: Document any breaking changes

### API Changes
- [ ] **Documentation**: Update API documentation if endpoints changed
- [ ] **Backward compatibility**: Ensure changes don't break existing clients
- [ ] **Response validation**: Test all response formats

### Security Review
- [ ] **Authentication**: Verify proper authentication requirements
- [ ] **Authorization**: Check role-based access controls
- [ ] **Input validation**: Ensure all inputs are properly validated
- [ ] **SQL injection**: Review for potential vulnerabilities

### Performance
- [ ] **Database queries**: Check for N+1 queries and optimize
- [ ] **Caching**: Add caching where appropriate
- [ ] **Response times**: Verify API response times are acceptable

### Git Workflow
- [ ] **Commit messages**: Use clear, descriptive commit messages
- [ ] **Branch naming**: Use feature/bugfix prefixes
- [ ] **Code review**: Have code reviewed before merging
- [ ] **Documentation updates**: Update README or docs if needed

### Deployment Readiness
- [ ] **Environment variables**: Check configuration settings
- [ ] **Dependencies**: Update requirements.txt if needed
- [ ] **Static files**: Ensure all assets are properly handled
- [ ] **Error handling**: Verify graceful error handling