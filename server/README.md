# Infinity Backend

A Spring Boot backend application built with Gradle for the Infinity project.

## Features

- **Spring Boot 3.2.1** with Java 17
- **Gradle** build system with wrapper
- **Spring Security** with CORS configuration
- **Spring Data JPA** with H2 database for development
- **Spring Boot DevTools** for hot reloading
- **Actuator** for monitoring endpoints
- **Lombok** for reducing boilerplate code

## Development Setup

### Prerequisites

- Java 17 or higher
- No need to install Gradle (uses Gradle wrapper)

### Running the Application

1. **Using Gradle Wrapper (Recommended):**
   ```bash
   # On Windows
   .\gradlew.bat bootRun
   
   # On Unix/Linux/macOS
   ./gradlew bootRun
   ```

2. **Or build and run:**
   ```bash
   # Build the application
   .\gradlew.bat build
   
   # Run the JAR
   java -jar build/libs/infinity-backend-0.0.1-SNAPSHOT.jar
   ```

### Development Features

- **Hot Reload**: Application automatically restarts when code changes are detected
- **H2 Console**: Available at http://localhost:8080/h2-console
  - JDBC URL: `jdbc:h2:mem:infinitydb`
  - Username: `sa`
  - Password: `password`
- **Health Endpoints**: 
  - Application health: http://localhost:8080/actuator/health
  - Application info: http://localhost:8080/actuator/info

### API Endpoints

#### Public Endpoints (No Authentication Required)

- `GET /api/public/health` - Application health check
- `GET /api/public/ping` - Simple ping endpoint
- `POST /api/public/echo` - Echo back the request payload

#### Examples

```bash
# Health check
curl http://localhost:8080/api/public/health

# Ping
curl http://localhost:8080/api/public/ping

# Echo
curl -X POST http://localhost:8080/api/public/echo \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello World"}'
```

### CORS Configuration

The application is configured to accept requests from:
- http://localhost:3000 (Next.js frontend)
- http://127.0.0.1:3000

### Database

- **Development**: H2 in-memory database
- **Production**: PostgreSQL (configured but not active in dev profile)

### Security

- Basic authentication is enabled for protected endpoints
- Default credentials: `admin/admin`
- Public endpoints under `/api/public/**` are accessible without authentication

### Building for Production

```bash
# Build the application
.\gradlew.bat build

# The JAR file will be created in build/libs/
```

### IDE Setup

For IntelliJ IDEA:
1. Import the project as a Gradle project
2. Make sure the project SDK is set to Java 17+
3. Enable annotation processing for Lombok

For VS Code:
1. Install the "Extension Pack for Java"
2. Open the server folder as the workspace root 