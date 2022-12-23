FROM docker.io/thoom/pyresttest

COPY ./tests /user/src/app

WORKDIR /user/src/app

ENTRYPOINT [ "pyresttest" ]

CMD ["https://za7img25p0.execute-api.us-east-2.amazonaws.com/","api_test.yml"]