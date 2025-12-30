# 第一階段：建置階段
FROM node:20-alpine as build

WORKDIR /app

# 複製 package.json 和 package-lock.json
COPY package*.json ./

# 安裝依賴
RUN npm install

# 複製專案檔案
COPY . .

# 建置 Vue 應用
RUN npm run build

# 第二階段：生產階段
FROM nginx:alpine

# 複製建置好的檔案到 nginx
COPY --from=build /app/dist /usr/share/nginx/html

# 複製 nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

# 啟動 nginx
CMD ["nginx", "-g", "daemon off;"]
