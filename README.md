# Auto Viber Bot

## Nội Dung
1. [Cài đặt](#setup) <br>

## 1. Cài đặt <a name="setup"></a>
### Cài đặt trực tiếp lên máy
```bash
pip install -r requirements.txt 
pip install -e .
```

Sau khi cài đặt, mở terminal trong ubuntu hoặc cmd trong window chạy lệnh:
```bash
./start_app.sh
```


### Cài đặt với Docker
Build docker từ thư mục chứa code:
```bash
docker build -t auto-viber-bot:1.0 -f Dockerfile .
```
**Hoặc** pull docker image từ docker hub về:
```bash
docker pull tuanlt175/auto-viber-bot:1.0
```

Tạo một thư mục chứa dữ liệu cho viber bot trên máy, sau đó copy 3 file trong thư mục `data` vào đó:
    - **service_config.yml**: thư mục chứa cấu hình cho service
    - **bot_config.yml**: File chứa cấu hình cho các viber bot
    - **message.txt**: File chứa nội dung tin nhắn bot sẽ gửi
    

Sau đó chạy lệnh dưới để chạy docker:
```bash
docker run -p 5005:5005 --network host \
    --name auto_viber_bot_container \
    -v <Thư mục chứa dữ liệu của viber bot trên máy>:/viber_bot/data \
    -it --rm auto-viber-bot:1.0
```
