# Journal
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-blue?logo=github)](https://github.com/sponsors/kevinveenbirkenbach) [![Patreon](https://img.shields.io/badge/Support-Patreon-orange?logo=patreon)](https://www.patreon.com/c/kevinveenbirkenbach) [![Buy Me a Coffee](https://img.shields.io/badge/Buy%20me%20a%20Coffee-Funding-yellow?logo=buymeacoffee)](https://buymeacoffee.com/kevinveenbirkenbach) [![PayPal](https://img.shields.io/badge/Donate-PayPal-blue?logo=paypal)](https://s.veen.world/paypaldonate)

This software is designed to manage a journal and create products, cvs and reports out of it. 

```bash
sudo docker-compose down && sudo docker-compose up --build --force-recreate -d
sudo docker volume rm $(sudo docker volume ls -q) 
sudo docker-compose exec -it web bash
```

```bash
rm -rv ./*/__pycache__
```