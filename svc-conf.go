package configurator

import (
	"context"
	"time"

	grpc_middleware "github.com/grpc-ecosystem/go-grpc-middleware"
	grpc_logrus "github.com/grpc-ecosystem/go-grpc-middleware/logging/logrus"
	grpc_opentracing "github.com/grpc-ecosystem/go-grpc-middleware/tracing/opentracing"
	grpc_prometheus "github.com/grpc-ecosystem/go-grpc-prometheus"
	opentracing "github.com/opentracing/opentracing-go"

	"github.com/sirupsen/logrus"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"

	lib "gitlab.com/SpoonQIR/Cloud/library/golang-common.git"
)

type ConfService struct {
	Confconn *grpc.ClientConn
	Confsvc  ConfiguratorClient
	Confreco chan bool

	Id *lib.Identity
}

// InitConf tst
func (s *ConfService) InitConf(authorizationHost string, tracer opentracing.Tracer, logger *logrus.Logger) chan bool {
	logentry := logrus.NewEntry(logger)
	logopts := []grpc_logrus.Option{
		grpc_logrus.WithDurationField(func(duration time.Duration) (key string, value interface{}) {
			return "grpc.time_ns", duration.Nanoseconds()
		}),
	}

	otopts := []grpc_opentracing.Option{
		grpc_opentracing.WithTracer(tracer),
	}

	var err error

	connect := make(chan bool)

	go func(lconn chan bool) {
		for {
			logrus.Info("Wait for connect")
			r := <-lconn
			logrus.WithFields(logrus.Fields{"reconn": r}).Info("conn chan receive")
			if r {
				for i := 1; i < 5; i++ {
					// s.authconn, s.Confsvc,
					s.Confconn, err = grpc.Dial(authorizationHost,
						grpc.WithInsecure(),
						grpc.WithUnaryInterceptor(grpc_middleware.ChainUnaryClient(
							grpc_logrus.UnaryClientInterceptor(logentry, logopts...),
							grpc_opentracing.UnaryClientInterceptor(otopts...),
							grpc_prometheus.UnaryClientInterceptor,
						)),
						grpc.WithStreamInterceptor(grpc_middleware.ChainStreamClient(
							grpc_logrus.StreamClientInterceptor(logentry, logopts...),
							grpc_opentracing.StreamClientInterceptor(otopts...),
							grpc_prometheus.StreamClientInterceptor,
						)),
					)
					if err != nil {
						logger.Fatalf("did not connect: %v, try : %d - sleep 5s", err, i)
						time.Sleep(2 * time.Second)
					} else {
						s.Confsvc = NewConfiguratorClient(s.Confconn)
						break
					}
				}
			} else {
				logrus.Info("end of goroutine - reconnect")
				return
			}
		}
	}(connect)

	logger.WithFields(logrus.Fields{"host": authorizationHost}).Info("Connexion au service gRPC 'Conf'")
	connect <- true
	return connect
}

func (s *ConfService) GetConf(ctx context.Context, usr *Conf) (*Conf, error) {
	for i := 1; i <= 5; i++ {
		grp, err := s.Confsvc.Get(ctx, usr)
		logrus.WithFields(logrus.Fields{"ctx.err": ctx.Err(), "err": err}).Trace("error ctx get object")
		if err != nil {
			logrus.WithFields(logrus.Fields{"err": err}).Error("error get object")
			errStatus, _ := status.FromError(err)
			if errStatus.Code() == codes.Unavailable {
				s.Confreco <- true
			} else if errStatus.Code() == codes.Canceled {
				s.Confreco <- true
			} else if errStatus.Code() == codes.DeadlineExceeded {
				s.Confreco <- true
			} else if errStatus.Code() == codes.Aborted {
				s.Confreco <- true
			} else if errStatus.Code() == codes.Unauthenticated {
				logrus.Info("ws-configurator not identified")
				return nil, status.Error(codes.Unauthenticated, "unauthenticated")
			} else if errStatus.Code() == codes.InvalidArgument {
				return nil, status.Errorf(codes.InvalidArgument, "argument invalid %v", err)
			} else if errStatus.Code() == codes.NotFound {
				return nil, nil
			}
			// errStatus.Code() == codes.Internal = retry
		} else if ctx.Err() != nil {
			s.Confreco <- true
		} else {
			return grp, nil
		}
	}
	return nil, status.Errorf(codes.NotFound, "authorization not found")
}
