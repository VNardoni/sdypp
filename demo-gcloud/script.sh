#!/bin/bash
# Update package lists
sudo apt update

# Install Node.js 18.x
sudo apt install -y nodejs




sudo apt install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx

sudo systemctl status nginx