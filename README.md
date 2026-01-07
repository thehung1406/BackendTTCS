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
│   │   └── database.py     # Kết nối DB
│   ├── models/             # Đinh nghĩa ORM models
│   ├── repositories/       # Tầng truy cập dữ liệu với DB
│   ├── services/           # Xử lý logic nghiệp vụ
│   ├── router/             # API endpoints
│   └── schemas/            # Dữ liệu Pydantic
├── .env                   # Biến môi trường
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker Compose config
├── alembic/               # Database migrations
│   ├── versions/          # Migration files
│   ├── env.py             # Alembic configuration
│   └── script.py.mako     # Migration template
├── alembic.ini            # Alembic config file
├── migrate.py             # Migration helper script
└── main.py               # FastAPI app entry point
```


