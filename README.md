# BackendTTCS - FastAPI + PostgreSQL

## Setup & Run với Docker

### Yêu cầu
- Docker
- Docker Compose

### Cách chạy

```bash
# Build và start services
docker-compose up --build

# Hoặc nếu muốn chạy ngầm
docker-compose up -d --build

# Xem logs
docker-compose logs -f api

# Xem logs PostgreSQL
docker-compose logs -f postgres
```

### URL API
- **API**: http://localhost:8000
- **Docs (Swagger)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **PostgreSQL**: localhost:5432

### Dừng services
```bash
docker-compose down
```

### Reset database
```bash
docker-compose down -v
docker-compose up --build
```

## Cấu trúc dự án

```
BackendTTCS/
├── app/
│   ├── core/
│   │   ├── config.py       # Settings từ .env
│   │   └── database.py     # Database connection & init
│   ├── models/             # SQLModel definitions
│   ├── repositories/       # Data access layer
│   ├── services/           # Business logic
│   ├── router/             # API endpoints
│   └── schemas/            # Request/Response schemas
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker Compose config
└── main.py               # FastAPI app entry point
```

## Database

Database được tạo tự động khi container khởi động:
1. PostgreSQL container tạo database từ `POSTGRES_DB` env
2. FastAPI app gọi `init_db()` để tạo tables từ models
3. SQLAlchemy sử dụng SQLModel metadata để tạo schema

## Troubleshooting

### Database không tạo
- Kiểm tra logs: `docker-compose logs postgres`
- Đảm bảo `.env` file có `DATABASE_URL` đúng
- Xóa volume cũ: `docker-compose down -v`

### API không khởi động
- Kiểm tra logs: `docker-compose logs api`
- Đảm bảo PostgreSQL khối động trước (health check)
- Xem `main.py` retry logic

### Port conflict
- Thay đổi port trong `docker-compose.yml`
- Ví dụ: `8001:8000` thay vì `8000:8000`

