# etapa de compilación
FROM node:9.11.1-alpine as build-stage
ARG VUE_APP_BACKEND_URI=http://localhost
ENV VUE_APP_BACKEND_URI=$VUE_APP_BACKEND_URI

RUN apk add --no-cache --virtual .gyp \
        python \
        make \
        g++
RUN apk update && \
    apk add --update git && \
    apk add --update openssh

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# etapa de producción
FROM nginx:1.13.12-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]