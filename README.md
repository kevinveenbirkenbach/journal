sudo docker-compose down && sudo docker-compose up --build --force-recreate -d

sudo docker volume rm $(sudo docker volume ls -q) 


sudo docker-compose exec -it backend bash
## todo 
.env müssen verändert werden