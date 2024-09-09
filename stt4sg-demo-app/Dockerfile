FROM node:14.17.0-alpine as build-step
RUN mkdir -p /app
WORKDIR /app
COPY package.json /app
RUN npm install
COPY . /app
RUN npm run build --prod

FROM nginx:1.21
COPY --from=build-step /app/dist/stt4sg-demo-app /usr/share/nginx/html
EXPOSE 80