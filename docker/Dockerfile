FROM node:16-alpine

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci 
# ci -> package-lock.json에 명시되어있는 버전을 똑같이 다운받는 것.
# install -> 최신 버전으로 다운받는 것. 

COPY index.js  .

ENTRYPOINT [ "node", "index.js"  ]
# node라는걸 실행할거고, index.js파일을 실행해.

# Dockerfile은 Layer형식으로 되어있음.
# 가장 빈번히 발생하는것을 가장 마지막에 입력해주기

# coker build -f Dockerfile -t fun-docker .
# . -> build context / 도커에게 너가 필요한 파일은 여기있어! / .은 최상위 경로
# f -> 어떤 도커파일을 사용할건지 명시
# t -> tag / 도커이미지에 이름을 부여할 수 있음 