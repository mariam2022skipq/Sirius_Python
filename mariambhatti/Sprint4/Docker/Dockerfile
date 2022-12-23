FROM docker.io/thoom/pyresttest

COPY ./tests /user/src/app

WORKDIR /user/src/app

ENTRYPOINT [ "pyresttest" ]

CMD ["https://ri1brbwhii.execute-api.us-east-2.amazonaws.com","api_test.yml"]