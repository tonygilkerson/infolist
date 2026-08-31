# info

Command line tool to search my info

## Setup

```sh
# init
go mod init github.com/tonygilkerson/infolist

# Should run automatically
direnv allow 
```

## Dev

```sh
# run
go run cmd/infolist/main list

# Install
go install ./cmd/infolist
```



## As a User


## Example Project

```sh
my-app/
├── cmd/
│   └── my-app/
│       └── main.go          # Application entry point
├── pkg/                     # (Optional) Library code suitable for external import
│   └── auth/
│       └── auth.go
├── internal/                # Private application code (enforced by Go toolchain)
│   ├── config/
│   │   └── config.go
│   ├── handler/
│   │   └── user.go
│   └── service/
│       └── user.go
├── api/                     # (Optional) OpenAPI/Swagger specs, Proto files
├── scripts/                 # (Optional) Build, installation, or analysis scripts
├── go.mod                   # Go module file
├── go.sum                   # Go checksum file
├── Makefile                 # Build targets and tasks
└── README.md
``