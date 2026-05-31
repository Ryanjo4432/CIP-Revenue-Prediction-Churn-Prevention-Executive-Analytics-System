FROM node:20-alpine

WORKDIR /app

COPY package.json .
RUN npm install

COPY . .

# 0.0.0.0 so vite dev server is reachable outside the container
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
