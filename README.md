# Hệ Thống Banking AI-Agent — Kiến Trúc Microservices (Lab 4)
### Họ và tên sinh viên: Vũ Duy Thụ
### MSSV: 23120093
### Môn học: Ứng dụng xử lí ngôn ngữ tự nhiên trong doanh nghiệp



Dự án triển khai một hệ thống **Banking AI-Agent đa dịch vụ** (Multi-service) hoàn chỉnh phục vụ lĩnh vực ngân hàng. Hệ thống áp dụng mô hình ngôn ngữ lớn (LLM - Ollama) để nhận diện ý định của khách hàng qua giao thức **gRPC** hiệu năng cao, định tuyến xử lý tự động theo **18 chính sách nghiệp vụ**, và soạn phản hồi tự động thông qua giao diện Chat trực quan.


---

## Kiến Trúc Hệ Thống (Architecture)

Hệ thống được thiết kế theo mô hình Microservices phân rã thành các dịch vụ độc lập giao tiếp qua mạng nội bộ Docker:

```
                    ┌────────────────────────┐
                    │  Frontend (Streamlit)  │
                    │      Cổng: 8501        │
                    └───────────┬────────────┘
                                │ HTTP (API Call)
                    ┌───────────▼────────────┐
                    │  API Gateway (FastAPI) │
                    │      Cổng: 8000        │
                    └─────┬──────────────┬───┘
            gRPC (50051)  │              │ HTTP (11434)
            ┌─────────────▼─┐      ┌─────▼──────────────┐
            │Intent Service │      │   Ollama Server    │
            │ (gRPC Server) │      │ (Google Colab/Local)│
            └───────────────┘      └────────────────────┘
```

### Chi Tiết Dịch Vụ (Services)

| Service | Công Nghệ | Cổng Mặc Định | Vai Trò |
|---------|-----------|---------------|---------|
| **Frontend** | Streamlit | `8501` | Giao diện Chat UI tương tác, hiển thị trực quan các bước xử lý ngầm (Workflow Details). |
| **API Gateway** | FastAPI | `8000` | Cổng tiếp nhận HTTP, điều phối quy trình Agentic Workflow đi qua các Node nghiệp vụ. |
| **Intent Service** | gRPC + Python | `50051` | Dịch vụ phân loại ý định (Intent) của khách hàng độc lập, giao tiếp với API Gateway qua gRPC. |
| **Ollama Service** | Ollama LLM | `11434` | Máy chủ chạy mô hình `gpt-oss:20b` (hoặc Qwen2.5) cung cấp trí tuệ nhân tạo (External). |

---

## Các Tính Năng Nổi Bật

1. **Nhận Diện 78 Nhóm Ý Định:** Khớp chính xác câu hỏi của khách hàng vào 77 ý định thuộc tập dữ liệu ngân hàng tiêu chuẩn **Banking77** + 1 ý định `general_inquiry`.
2. **Quy Trình Nghiệp Vụ Tự Động (6 Nodes):**
   * **Intent Node:** Lấy kết quả phân loại ý định từ gRPC service.
   * **Priority Node:** Tự động đánh giá độ khẩn cấp (`LOW`, `MEDIUM`, `HIGH`, `URGENT`).
   * **Policy Node:** Áp dụng chính xác 1 trong **18 Chính sách ngân hàng** mẫu phù hợp nhất.
   * **Validation Node:** Kiểm duyệt câu trả lời của AI để đảm bảo an toàn tài chính.
   * **Router Node:** Định tuyến hồ sơ về đúng phòng ban chuyên trách (ví dụ: Chống gian lận, Tín dụng, Hỗ trợ thẻ).
   * **Draft Node:** Sử dụng LLM tổng hợp thông tin và soạn thảo thư nháp hoàn hảo gửi khách hàng.
3. **Cơ Chế Dự Phòng (Fallback) Thông Minh:** Nếu máy chủ AI (Ollama) ngoại tuyến, hệ thống không bị sập hay treo mà tự động kích hoạt chế độ Fallback: gán độ ưu tiên `HIGH`, đánh dấu kiểm duyệt `Failed` và đề xuất chuyển giao ngay cho nhân viên hỗ trợ (`escalate_to_agent`).

---

## Hướng Dẫn Khởi Chạy Hệ Thống

---

### Chạy Bằng Docker Compose

#### Bước 1: Khởi động máy chủ Ollama LLM

* **Chạy trên Google Colab:**
  1. Mở Notebook Colab chạy Ollama của bạn và khởi động GPU.
  2. Tạo đường hầm mạng thông qua Pinggy để lấy Public URL. Ví dụ: `https://xxxx.run.pinggy-free.link`.
  3. Mở file `docker-compose.yml` ở thư mục gốc dự án.
  4. Sửa giá trị biến môi trường `OLLAMA_BASE_URL` của cả 2 service `backend` và `intent-service` thành link Pinggy của bạn:
     ```yaml
     OLLAMA_BASE_URL: https://xxxx.run.pinggy-free.link
     ```

#### Bước 2: Build các Container của hệ thống
Mở terminal (PowerShell) tại thư mục gốc của dự án (`banking-service/`) và chạy:
```powershell
docker compose build
```

#### Bước 3: Khởi chạy hệ thống
Chạy lệnh sau để bật toàn bộ các container chạy ngầm:
```powershell
docker compose up -d
```

#### Bước 4: Kiểm tra trạng thái hoạt động
```powershell
docker ps
```
Cả 3 container `banking-frontend`, `banking-backend`, và `intent-service` phải ở trạng thái **`Up`**.

---

## Kiểm Tra & Trải Nghiệm Ứng Dụng

Sau khi khởi chạy thành công theo một trong hai cách trên, hãy mở trình duyệt của bạn:

* **Giao diện Chat trực quan (Streamlit UI):** Truy cập **`http://localhost:8501`**
* **Tài liệu API chi tiết (FastAPI Swagger):** Truy cập **`http://localhost:8000/docs`**

### Một số câu hỏi có thể tham khảo:
  > `"I lost my credit card at the shopping mall today, please lock it immediately to prevent fraud!"`

  > `"The ATM machine just swallowed my debit card and it won't come out. What do I do now?"`

  > `"I entered my card PIN incorrectly three times and now my debit card is blocked. How do I unblock it?"`

---

## Cấu Trúc Thư Mục Dự Án (Project Structure)

Dự án tuân thủ chính xác 100% sơ đồ cấu trúc file chuẩn được yêu cầu trong tài liệu đồ án của HCMUS với các đường liên kết trực quan:

```text
banking-service/
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   │   └── orchestrator.py        # Luồng chạy chính (Agentic pipeline)
│   │   ├── clients/
│   │   │   ├── base.py
│   │   │   ├── grpc_intent_client.py   # Client kết nối gRPC
│   │   │   ├── intent_grpc/            # Thư mục chứa code gRPC sinh ra từ Makefile
│   │   │   │   ├── intent_service_pb2_grpc.py
│   │   │   │   └── intent_service_pb2.py
│   │   │   └── ollama_client.py        # Kết nối HTTP tới Ollama
│   │   ├── core/
│   │   │   ├── schemas.py              # Định nghĩa cấu trúc Pydantic
│   │   │   └── settings.py             # Quản lý cấu hình & biến môi trường
│   │   ├── data/
│   │   │   └── policies.py             # Chứa 18 chính sách ngân hàng mẫu
│   │   ├── main.py                     # Điểm khởi chạy API Gateway FastAPI
│   │   └── nodes/                      # Các node xử lý thông tin độc lập
│   │       ├── draft_node.py
│   │       ├── intent_node.py
│   │       ├── policy_node.py
│   │       ├── priority_node.py
│   │       ├── router_node.py
│   │       └── validation_node.py
│   ├── Dockerfile
│   ├── README.md                       # Hướng dẫn riêng cho backend
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── Dockerfile
│   ├── interface.py                    # Giao diện Streamlit Chat UI
│   └── requirements.txt
├── intent_service/
│   ├── app/                            # Ý định phân loại logic
│   │   ├── clients/
│   │   │   ├── base.py
│   │   │   └── ollama_client.py
│   │   ├── core/
│   │   │   ├── schemas.py
│   │   │   └── settings.py
│   │   ├── data/
│   │   │   └── policies.py
│   │   └── nodes/
│   │       └── intent_node.py
│   ├── client.py                       # File test client gRPC nhanh
│   ├── Dockerfile
│   ├── intent_service_pb2_grpc.py      # Code gRPC sinh từ Makefile
│   ├── intent_service_pb2.py           # Code gRPC sinh từ Makefile
│   ├── intent_service.proto            # File định nghĩa dịch vụ gRPC
│   ├── Makefile                        # Tự động hóa biên dịch gRPC stubs
│   ├── requirements.txt
│   └── server.py                       # gRPC Server chính chạy cổng 50051
├── docker-compose.yml                  # File cấu hình Docker Compose chính
└── README.md                           # File hướng dẫn này (Tiếng Việt)
```

---

## Video Demo
- **Link video demo:** [Link Video Youtube](https://youtu.be/-6g47z0Zb9E)

---
