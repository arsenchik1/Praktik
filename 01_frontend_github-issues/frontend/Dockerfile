FROM node:18-alpine

WORKDIR /app

# Копируем package.json
COPY package.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем остальные файлы
COPY . .

# Создаем .env файл с токеном (передается через ARG)
ARG REACT_APP_GITHUB_TOKEN
ENV REACT_APP_GITHUB_TOKEN=$REACT_APP_GITHUB_TOKEN

EXPOSE 3000

CMD ["npm", "start"]