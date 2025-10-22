# Code Structure and Architecture

## Project Directory Structure
```
GameMarketplace/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── models/         # SQLAlchemy models (all in __init__.py)
│   │   ├── api/           # API endpoints
│   │   │   ├── auth.py    # Authentication endpoints
│   │   │   ├── users.py   # User management
│   │   │   ├── games.py   # Game catalog
│   │   │   ├── lots.py    # Item listings
│   │   │   └── orders.py  # Order processing
│   │   ├── core/          # Core configuration
│   │   │   ├── config.py  # Application settings
│   │   │   ├── database.py # Database setup
│   │   │   └── auth.py    # Authentication utilities
│   │   ├── services/      # Business logic (empty)
│   │   └── utils/         # Helper functions (empty)
│   ├── tests/             # Tests
│   └── migrations/        # Database migrations
├── frontend/              # React frontend (structure only)
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── hooks/         # Custom hooks
│   │   ├── services/      # API services
│   │   ├── store/         # State management
│   │   ├── types/         # TypeScript types
│   │   └── styles/        # Styling
│   └── public/            # Static files
├── database/              # SQL schemas and scripts
├── static/                # Media files and uploads
└── docs/                  # Documentation
```

## Database Models
- **User**: Authentication, profile, stats, role-based access
- **Game**: Game catalog with metadata and images
- **Category**: Item categories per game with hierarchical structure
- **Lot**: Items for sale with details and status
- **Order**: Purchase orders with escrow and status tracking
- **Message**: Chat system for user communication
- **Review**: Rating and review system

## API Architecture
- RESTful API design with FastAPI
- Authentication with JWT tokens
- Role-based access control (User, Seller, Moderator, Admin)
- Proper error handling and validation
- CORS configured for frontend integration
- Static file serving for uploads