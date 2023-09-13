# Journal
This software is designed to manage a journal and create products, cvs and reports out of it. 

```bash
sudo docker-compose down && sudo docker-compose up --build --force-recreate -d
sudo docker volume rm $(sudo docker volume ls -q) 
sudo docker-compose exec -it web bash
```

```bash
rm -rv ./*__pycache__
```