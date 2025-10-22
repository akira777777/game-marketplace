# GameMarketplace Project Overview

## Purpose
GameMarketplace is a modern trading platform for gaming items and services, inspired by FunPay but with improved UX/UI and modern technologies. It serves as a secure marketplace for buying and selling gaming assets with features like:

- Game catalog with popular games
- Secure trading through escrow system
- Built-in chat between users
- Review and rating system
- Smart search with advanced filters
- Responsive design
- Dark theme

## Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Database (currently configured, can be changed to PostgreSQL)
- **WebSocket** - Real-time chat functionality
- **JWT** - Secure authentication
- **Redis** - Caching and sessions (configured but optional)
- **Pydantic** - Data validation

### Frontend
- **React 18** - Modern UI library
- **TypeScript** - Typed JavaScript
- **Vite** - Fast build tool
- **TailwindCSS** - Utility-first CSS
- **React Query** - Server state management
- **React Router** - Routing

## Features
- User authentication and authorization
- Game catalog management
- Lot/item listing and management
- Order processing with escrow
- Real-time chat system
- Review and rating system
- File upload for images
- Admin panel functionality

## Current Status
- Backend is fully implemented and functional
- Database models are comprehensive and well-designed
- API endpoints are defined for all major functionality
- Frontend structure exists but requires implementation
- Server is currently running successfully on port 8001