#!/bin/bash

set -e

python3 -m pip install grpcio
python3 -m pip install grpcio-tools


GEN_PATH="."
GO_LIB_PATH=$(go env GOPATH)/src
GOPATH=$(go env GOPATH)

GROUPS_VERSION="master"
curl -o proto/groups.proto "https://raw.githubusercontent.com/slavayssiere-spoon/groups/$GROUPS_VERSION/proto/groups.proto"

ROBOTS_VERSION="master"
curl -o proto/robots.proto "https://raw.githubusercontent.com/slavayssiere-spoon/robots/$ROBOTS_VERSION/proto/robots.proto"

echo "gen protoc golang"
protoc \
        -I proto \
        -I $GO_LIB_PATH/include \
        --go_out=$GEN_PATH      --go_opt=paths=source_relative \
        --go-grpc_out=$GEN_PATH --go-grpc_opt=paths=source_relative \
        --grpc-gateway_out=logtostderr=true,paths=source_relative:$GEN_PATH \
        --openapiv2_out=logtostderr=true:$GEN_PATH \
        proto/conf.proto

protoc-go-inject-tag -input=./conf.pb.go

echo "mod tidy"
go mod tidy

echo "update"
go get -u ./...


GEN_PATH="configurator"
mkdir -p $GEN_PATH

echo "launch protoc python"

python3 -m grpc_tools.protoc \
        -I proto \
        -I $GOPATH/src/include \
        --python_out=$GEN_PATH \
        $GOPATH/src/include/protoc-gen-openapiv2/options/annotations.proto

python3 -m grpc_tools.protoc \
        -I proto \
        -I $GOPATH/src/include \
        --python_out=$GEN_PATH \
        $GOPATH/src/include/protoc-gen-openapiv2/options/openapiv2.proto

python3 -m grpc_tools.protoc \
        -I proto \
        -I $GOPATH/src/include \
        --python_out=$GEN_PATH \
        --grpc_python_out=$GEN_PATH \
        proto/conf.proto

protoc \
        -I proto \
        -I $GOPATH/src/include \
        --openapiv2_out=logtostderr=true:$GEN_PATH \
        proto/conf.proto
