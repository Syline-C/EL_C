
.PHONY: help
help:
	@echo "Targets:"
	@echo "  make start         # conda env 생성(레이어 순차 적용)"
	@echo "  make stop          # + GPU 레이어(Pytorch or TF 중 택1) 적용"
	@echo "  make remove        # 환경 export (environment.lock.yml)"
	@echo "  make build         # Docker 이미지 빌드(호스트 TZ 반영)"
	@echo "  make run-gpu       # GPU 사용 실행"
	@echo "  make run-cpu       # CPU 실행"
	@echo "  make jupyter       # JupyterLab 컨테이너 실행"
	@echo "  make retro-import  # ROM 디렉터리 등록"
	@echo "  make smoke         # 스모크 임포트 테스트(컨테이너 내부)"
	@echo "  make clean         # 이미지/컨테이너 정리(위험 주의)"



.PHONY:start
start:
	./docker/00_startDocker.sh

.PHONY:stop
stop:
	./docker/01_stopDocker.sh

.PHONY:remove
remove:
	./docker/02_removeDockerEnv.sh
