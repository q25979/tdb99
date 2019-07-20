FROM node:7-alpine
RUN mkdir -p /usr/local/icaimall-fe
COPY ./dist/final/ /usr/local/icaimall-fe/
WORKDIR /usr/local/icaimall-fe
EXPOSE 5000
ENV NODE_ENV production
CMD ["npm", "start"]
