┌─────────────────────────────────────┐
│ HTTP Server Layer │
│ ┌──────────┐ ┌─────────────┐ │
│ │ Proxy │------->│ Backend │ │
│ │ :8080 │ │ :9000 │ │
│ └──────────┘ └─────────────┘ │
└─────────────────────────────────────┘
-----Proxy------

->create_proxy(Entry point để chạy proxy từ start_proxy.py.)
->run_proxy(Khởi chạy proxy, tạo socket, lắng nghe kết nối, spawn thread cho từng client.)
->handle_client(Xử lý từng request từ client — đọc request, xác định Host, tìm backend, chuyển tiếp, gửi lại response.)
->resolve_routing_policy()
->forward_request

-----Backend------
